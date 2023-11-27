INSERT INTO letter_grades
VALUES
    ('A', 4),
    ('B', 3),
    ('C', 2),
    ('D', 1),
    ('F', 0);

INSERT INTO name_mapping
VALUES
    ('1143956280222957578', 'cornonjacob', 'Jacob Gerlach');

INSERT INTO previous_course_grades
VALUES
    ('cornonjacob', 'CSC510', 'A'),
    ('cornonjacob', 'CSC540', 'B');

INSERT INTO grade_bounds
VALUES
    ('A', 90, 100),
    ('B', 80, 89),
    ('C', 70, 79),
    ('D', 60, 69),
    ('F', 0, 59);

INSERT INTO grade_categories
VALUES
    (1, '1143956280222957578', 'project', 0.200),
    (3, '1143956280222957578', 'test', 0.700),
    (4, '1143956280222957578', 'hw', 0.100);

INSERT INTO assignments
VALUES
    (1, '1143956280222957578', 3, 'midterm1', 95),
    (2, '1143956280222957578', 1, 'project1', 100),
    (4, '1143956280222957578', 4, 'hw1', 100);

INSERT INTO grades
VALUES
    ('1143956280222957578', 'Ethical Software Enginnering', 1, 92),
    ('1143956280222957578', 'Software Testing', 2, 70),
    ('1143956280222957578', 'Version Controlling in SE', 4, 90);

INSERT INTO resources
VALUES
    ('1143956280222957580', 'Ethical Software Enginnering', 'https://github.com/txt/se23/blob/main/docs/ethics.md'),
    ('1143956280222957580', 'Software Testing', 'https://github.com/txt/se23/blob/main/docs/testing1.md'),
    ('1143956280222957580', 'Version Controlling in SE', 'https://github.com/txt/se23/blob/main/docs/cloud.md');

