SELECT
    current_club,
    AVG(age) AS AverageAge,
    AVG(appearances_current_club) AS AverageAppearances,
    COUNT(*) AS TotalPlayers
FROM players
GROUP BY current_club;