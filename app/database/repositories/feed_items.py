from typing import Optional, List, Iterable
from ..base import BaseRepository

import json
import base64
from datetime import datetime


class FeedRepository(BaseRepository):

    # =========================================================
    # ЛЕНТА (CARD)
    # =========================================================
    async def get_feed_items(
        self,
        cursor: Optional[str] = None,  # теперь cursor — base64 строка с {published_at, id}
        limit: int = 10,
        types: Optional[List[str]] = None,
        user_id: Optional[int] = None,
        include_favourites: bool = False,
        q: Optional[str] = None
    ) -> list[dict]:

        args = [user_id or 0]
        or_conditions = []
        and_conditions = []

        # --- OR: источники ---
        if types:
            or_conditions.append(f"f.type = ANY(${len(args)+1}::text[])")
            args.append(types)
        if include_favourites:
            and_conditions.append("uf.user_id IS NOT NULL")

        # --- AND: поиск ---
        if q:
            and_conditions.append(
                f"(c.title ILIKE ${len(args)+1} OR c.short_description ILIKE ${len(args)+1})"
            )
            args.append(f"%{q}%")

        # --- AND: курсор keyset ---
        if cursor:
            # декодируем cursor
            decoded = json.loads(base64.b64decode(cursor).decode())
            cursor_published_at = datetime.fromisoformat(decoded["published_at"])
            cursor_id = decoded["id"]

            and_conditions.append(
                f"(f.published_at < ${len(args)+1} OR (f.published_at = ${len(args)+1} AND f.id < ${len(args)+2}))"
            )
            args.extend([cursor_published_at, cursor_id])

        # --- собираем WHERE ---
        where_clauses = []
        if or_conditions:
            where_clauses.append("(" + " OR ".join(or_conditions) + ")")
        if and_conditions:
            where_clauses.extend(and_conditions)

        base_query = """
        SELECT
            f.id,
            f.type,
            f.published_at,
            c.title,
            c.short_description,
            c.body,
            c.preview_media_id,
            uf.user_id IS NOT NULL AS is_favourite,
            sp.selection_type
        FROM feed_items f
        LEFT JOIN feed_item_content c ON c.feed_item_id = f.id
        LEFT JOIN user_favourites uf
            ON uf.feed_item_id = f.id AND uf.user_id = $1
        LEFT JOIN selection_posts sp ON sp.feed_item_id = f.id
        """

        if where_clauses:
            base_query += " WHERE " + " AND ".join(where_clauses)

        base_query += f"""
        ORDER BY f.published_at DESC, f.id DESC
        LIMIT ${len(args)+1}
        """
        args.append(limit)

        return await self.fetch(base_query, *args)


    # =========================================================
    # BATCH MEDIA (ключевая часть)
    # =========================================================
    async def get_media_by_ids(
        self,
        media_ids: Iterable[int],
    ) -> dict[int, dict]:
        """
        Возвращает {media_id: media_row}
        """
        media_ids = list({mid for mid in media_ids if mid})
        if not media_ids:
            return {}

        rows = await self.fetch(
            """
            SELECT
                id,
                type,
                url,
                preview_url,
                width,
                height,
                duration_seconds
            FROM media_items
            WHERE id = ANY($1::bigint[])
            """,
            media_ids,
        )

        return {row["id"]: row for row in rows}

    # =========================================================
    # DETAIL (PAGE)
    # =========================================================
    async def get_feed_item_detail(self, feed_item_id: int, user_id: int) -> Optional[dict]:

        post = await self.fetchrow(
            """
            SELECT
                f.id,
                f.type,
                f.published_at,
                f.status,
                c.title,
                c.short_description,
                c.body,
                c.preview_media_id,
                b.text AS button_text,
                b.link AS button_link,
                uf.user_id IS NOT NULL AS is_favourite
            FROM feed_items f
            LEFT JOIN feed_item_content c ON c.feed_item_id = f.id
            LEFT JOIN user_favourites uf
            ON uf.feed_item_id = f.id AND uf.user_id = $1
            LEFT JOIN feed_item_buttons b ON b.feed_item_id = f.id
            WHERE f.id = $2
            """,
            user_id, feed_item_id
        )

        if not post:
            return None

        # ---------------------------
        # media (batch by feed_item)
        # ---------------------------
        media = await self.fetch(
            """
            SELECT
                m.id,
                m.type,
                m.url,
                m.preview_url,
                m.width,
                m.height,
                m.duration_seconds
            FROM feed_item_media fm
            JOIN media_items m ON m.id = fm.media_item_id
            WHERE fm.feed_item_id = $1
            ORDER BY fm.position
            """,
            feed_item_id,
        )
        post["media"] = media

        # ---------------------------
        # selection
        # ---------------------------
        if post["type"] == "selection":

            selection = await self.fetchrow(
                """
                SELECT selection_type
                FROM selection_posts
                WHERE feed_item_id = $1
                """,
                feed_item_id,
            )
            post["selection_type"] = selection["selection_type"] if selection else None

            # properties — ТОЛЬКО для single
            if selection and selection["selection_type"] == "single":
                post["properties"] = await self.fetch(
                    """
                    SELECT
                        p.id,
                        p.name,
                        ST_Y(p.location::geometry) AS latitude,
                        ST_X(p.location::geometry) AS longitude,
                        p.address,
                        p.city
                    FROM selection_properties sp
                    JOIN properties p ON p.id = sp.property_id
                    WHERE sp.feed_item_id = $1
                    ORDER BY sp.position
                    """,
                    feed_item_id,
                )
            else:
                post["properties"] = []

            # related selections (без media)
            if selection:
                post["related_selections"] = await self.fetch(
                    """
                    SELECT
                        f.id,
                        f.published_at,
                        c.title,
                        c.short_description,
                        c.preview_media_id,
                        uf.user_id IS NOT NULL AS is_favourite
                    FROM related_selections rs
                    JOIN feed_items f ON f.id = rs.related_feed_item_id
                    LEFT JOIN feed_item_content c ON c.feed_item_id = f.id
                    LEFT JOIN user_favourites uf
                        ON uf.feed_item_id = f.id AND uf.user_id = $1
                    WHERE rs.parent_feed_item_id = $2
                    ORDER BY rs.position
                    """,
                    user_id, feed_item_id
                )
            else:
                post["related_selections"] = []

        if post["type"] == "education":
            # ---------------------------
            # authors
            # ---------------------------
            
            post["authors"] = await self.fetch(
                """
                SELECT
                    a.id,
                    a.name
                FROM course_authors ca
                JOIN authors a ON a.id = ca.author_id
                LEFT JOIN media_items m ON m.id = a.avatar_media_id
                WHERE ca.feed_item_id = $1
                ORDER BY a.id
                """,
                feed_item_id,
            )

            # ---------------------------
            # lessons
            # ---------------------------
            lessons = await self.fetch(
                """
                SELECT
                    l.id,
                    l.title,
                    l.position,
                    COALESCE(SUM(m.duration_seconds), 0) AS duration_seconds,
                    EXISTS (
                        SELECT 1
                        FROM user_lesson_progress ulp
                        WHERE ulp.lesson_id = l.id
                          AND ulp.user_id = $2
                          AND ulp.completed = TRUE
                    ) AS is_checked
                FROM lessons l
                LEFT JOIN lesson_media lm ON lm.lesson_id = l.id
                LEFT JOIN media_items m ON m.id = lm.media_item_id
                WHERE l.course_feed_item_id = $1
                GROUP BY l.id
                ORDER BY l.position
                """,
                feed_item_id,
                user_id,
            )

            post["lessons"] = lessons


        return post

    async def get_feed_item_types(self) -> list[dict]:
        """
        Получить список категорий постов (для фильтров на фронте)
        """
        return await self.fetch("""
            SELECT code, title
            FROM feed_item_types
            ORDER BY id
        """)