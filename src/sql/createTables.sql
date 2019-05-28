/* Some stubs of potential tables. Nothing is concrete yet. */


/* One of the questions we know how to answer */
CREATE TABLE question (
    id            INT PRIMARY KEY,
    question_text TEXT,
    area          TEXT,
    response      TEXT
);

/* Used to store a query that the user asked for debugging */
CREATE TABLE user_query (
    id                INT PRIMARY KEY,
    time_asked        TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    query_text        TEXT,
    matched_question  INT REFERENCES question(id),
    correct           BOOLEAN
);



/*
Example Data Point (from website)

CSC 344. Music Programming. 4 units
Term Typically Offered: TBD
Prerequisite: CSC 141 or CSC 348; and CPE/CSC 357.
Music-producing programs. Software synthesizers: oscillators, coupled oscillators, wavetable synthesis. Sound processing units/filters: LTI, FIR, IIR, nonlinear. Physics of sound, mathematical foundations of sound synthesis and filtering, existing sound formats (both sampled and MIDI). 3 lectures, 1 laboratory.
*/
CREATE TABLE course (
    course_number     SMALLINT,
    course_area       VARCHAR(4),
    course_descrption TEXT,
    course_units      SMALLINT,
    PRIMARY KEY(course_number, course_area)
);

CREATE TABLE quarter (
    quarter_id            SMALLINT,
    quarter_name          VARCHAR(10),
    quarter_abbreviation  VARCHAR(2),
    PRIMARY KEY (quarter_id)
);

CREATE TABLE offered_in (
    course_number     SMALLINT REFERENCES course(course_number),
    course_area       VARCHAR(4) REFERENCES course(course_area),
    quarter_id        INT,
    PRIMARY KEY (course_number, course_area, quarter_id)
);