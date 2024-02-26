SELECT
    *,
    CASE
        WHEN age <= 23 THEN 'Young'
        WHEN age BETWEEN 24 AND 32 THEN 'MidAge'
        WHEN age >= 33 THEN 'Old'
    END AS AgeCategory,
    CASE
        WHEN appearances_current_club > 0 THEN CAST(goals_current_club AS FLOAT) / appearances_current_club
        ELSE 0
    END AS GoalsPerClubGame
FROM players;