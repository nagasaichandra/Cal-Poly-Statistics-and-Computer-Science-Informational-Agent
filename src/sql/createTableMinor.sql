CREATE TABLE cs_minor_info (
    division_units              TEXT,
    minor_general_requirements  TEXT,
    minor_flowchart_link        TEXT,
    required_courses TEXT,
    steps TEXT,
    minimum_gpa TEXT,
    prerequisites TEXT,
    application_link TEXT,
    required_units TEXT,
    approved_elective_units TEXT
);

CREATE TABLE minor_courses(
minor                   TEXT,
minor_courses           TEXT
);

CREATE TABLE concentration(
concentration_required_courses          TEXT,
concentration_list                      TEXT
);