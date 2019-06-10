CREATE TABLE course_types (
    course_number   SMALLINT,
    course_area     VARCHAR(7),
    course_name     VARCHAR(250),
    support_type     VARCHAR(150),
    PRIMARY KEY(course_number, course_area, support_type)
);

CREATE TABLE support_reqs (
    support_type    VARCHAR(150),
    units_reqs      SMALLINT,
    PRIMARY KEY (support_type)
)