DROP TABLE IF EXISTS reminders CASCADE;
DROP TABLE IF EXISTS grade_categories CASCADE;
DROP TABLE IF EXISTS assignments CASCADE;
DROP TABLE IF EXISTS grades CASCADE;
DROP TABLE IF EXISTS group_members CASCADE;
DROP TABLE IF EXISTS project_groups CASCADE;
DROP TABLE IF EXISTS name_mapping CASCADE;
DROP TABLE IF EXISTS pinned_messages CASCADE;
DROP TABLE IF EXISTS review_questions CASCADE;
DROP TABLE IF EXISTS questions CASCADE;
DROP TABLE IF EXISTS answers CASCADE;
DROP TABLE IF EXISTS group_settings CASCADE;
DROP TABLE IF EXISTS resources CASCADE;
DROP TABLE IF EXISTS previous_course_grades;
DROP TABLE IF EXISTS grade_bounds;
DROP TABLE IF EXISTS letter_grades;


CREATE TABLE reminders (
    guild_id        BIGINT NOT NULL,
    author_id       BIGINT NOT NULL,
    course          VARCHAR NOT NULL,
    reminder_name   VARCHAR NOT NULL,
    due_date        TIMESTAMP WITH TIME ZONE NOT NULL
);


CREATE TABLE grade_categories(
    id              bigserial primary key,
    guild_id        BIGINT NOT NULL,
    category_name   VARCHAR NOT NULL,
    category_weight DECIMAL(3, 3)

);

CREATE TABLE assignments (
    id              bigserial primary key,
    guild_id        BIGINT NOT NULL,
    category_id     BIGINT NOT NULL REFERENCES grade_categories(id) ON DELETE CASCADE,
    assignment_name VARCHAR NOT NULL,
    points          INTEGER NOT NULL DEFAULT 100

);

CREATE TABLE grades (
    guild_id        BIGINT NOT NULL,
    member_name     VARCHAR NOT NULL,
    assignment_id   INT NOT NULL REFERENCES assignments(id) ON DELETE CASCADE,
    grade           INT NOT NULL
);

CREATE TABLE group_members (
    guild_id        BIGINT NOT NULL,
    group_num       INTEGER NOT NULL,
    member_name     VARCHAR NOT NULL
);

CREATE TABLE project_groups (
    guild_id        BIGINT NOT NULL,
    project_num     INTEGER NOT NULL,
    group_num       INTEGER NOT NULL
);

CREATE TABLE name_mapping (
    guild_id        BIGINT NOT NULL,
    username        VARCHAR NOT NULL,
    real_name       VARCHAR NOT NULL
);

CREATE TABLE pinned_messages (
    guild_id        BIGINT NOT NULL,
    author_id       BIGINT NOT NULL,
    tag             VARCHAR NOT NULL,
    description     VARCHAR NOT NULL
);

CREATE TABLE review_questions (
    guild_id        BIGINT NOT NULL,
    question        VARCHAR NOT NULL,
    answer          VARCHAR NOT NULL
);

CREATE TABLE questions (
    guild_id        BIGINT NOT NULL,
    number          BIGINT NOT NULL,
    question        VARCHAR NOT NULL,
    author_id       BIGINT,
    msg_id          BIGINT NOT NULL,
    is_ghost        BOOLEAN DEFAULT false
);

CREATE TABLE answers (
    guild_id        BIGINT NOT NULL,
    q_number        BIGINT NOT NULL,
    answer          VARCHAR NOT NULL,
    author_id       BIGINT,
    author_role     VARCHAR NOT NULL
);

CREATE TABLE group_settings (
    guild_id        BIGINT NOT NULL,
    total_groups    INT NOT NULL,
    max_members     INT NOT NULL
);

CREATE TABLE resources(
    guild_id        BIGINT NOT NULL,
    topic_name      VARCHAR NOT NULL,
    resource_link   VARCHAR NOT NULL    
);

CREATE TABLE letter_grades (
    letter CHAR(2) PRIMARY KEY,
    grade_point FLOAT UNIQUE NOT NULL
);

CREATE TABLE previous_course_grades (
    member_name VARCHAR,
    course_id VARCHAR(32),
    course_grade CHAR(2) NOT NULL,
    PRIMARY KEY(member_name, course_id)
);

CREATE TABLE grade_bounds (
    grade_letter CHAR(2) PRIMARY KEY,
    lower_bound FLOAT UNIQUE NOT NULL,
    upper_bound FLOAT UNIQUE NOT NULL,
    FOREIGN KEY(grade_letter) REFERENCES letter_grades(letter) ON UPDATE CASCADE ON DELETE CASCADE
);
