CREATE TABLE division_levels (
    division_level VARCHAR(50),
    num_units_lower int,
    num_units_upper int,
    PRIMARY KEY (division_level)
);


CREATE TABLE class_levels (
    class_level VARCHAR(50),
    num_units_lower int,
    num_units_upper int,
    PRIMARY KEY (class_level)
);