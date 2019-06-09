CREATE TABLE course_types (
    course_number   SMALLINT,
    course_area     VARCHAR(4),
    course_type     VARCHAR(50),
    PRIMARY KEY(course_number, course_area),
    FOREIGN KEY(course_number, course_area) REFERENCES course(course_number, course_area)
);