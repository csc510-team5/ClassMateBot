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
)

CREATE TABLE resources(
    guild_id        BIGINT NOT NULL,
    topic_name      VARCHAR NOT NULL,
    resource_link       VARCHAR NOT NULL    
)