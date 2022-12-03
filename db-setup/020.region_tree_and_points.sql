-- region_tree: tree paths from bottom to top for each region
CREATE
MATERIALIZED VIEW region_tree AS (
	WITH RECURSIVE region_tree(name, slug, path) AS (
		-- start with root regions which don't have parents
		SELECT r.name, r.slug, array[r.slug]
		FROM regions r
		WHERE r.parent_slug IS NULL
	UNION ALL
		-- recursively, append to each region's path its parent's path
		SELECT r.name, r.slug, r.slug || rt.path
		FROM regions r, region_tree rt
		WHERE r.parent_slug = rt.slug
	)
	SELECT * FROM region_tree
);

-- points: A union of ports and regions treated as analogous entities with a code and a path.
CREATE
MATERIALIZED VIEW points AS (
        SELECT po.code AS code, po.code || rt.path AS path
        FROM ports po
        LEFT JOIN region_tree rt ON po.parent_slug = rt.slug
    UNION ALL
        SELECT rt.slug AS code, rt.path AS path
        FROM region_tree rt
);
