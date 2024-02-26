SELECT
    p1.name AS PlayerName,
    p1.positions AS PlayerPosition,
    p1.age AS PlayerAge,
    p1.appearances_current_club AS PlayerAppearances,
    (
        SELECT COUNT(*)
        FROM players p2
        WHERE p2.age < p1.age
        AND p2.positions = p1.positions
        AND p2.appearances_current_club > p1.appearances_current_club
    ) AS YoungerPlayersWithMoreAppearances
FROM players p1
WHERE p1.current_club = 'Liverpool';