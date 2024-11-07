-- Establecer country_id como llave primaria en country_dim
ALTER TABLE country_dim
    ADD CONSTRAINT pk_country PRIMARY KEY (country_id);

--relacion fact_table con country_dim
ALTER TABLE fact_table
    ADD CONSTRAINT fk_country
        FOREIGN KEY (country_id) REFERENCES country_dim(country_id);

-- Establecer country_id como llave primaria en country_dim
ALTER TABLE date_dim
    ADD CONSTRAINT pk_date PRIMARY KEY (date_id);

--relacion fact_table con country_dim
ALTER TABLE fact_table
    ADD CONSTRAINT fk_date
        FOREIGN KEY (date_id) REFERENCES date_dim(date_id);

-- Establecer country_id como llave primaria en country_dim
ALTER TABLE people_dim
    ADD CONSTRAINT pk_people PRIMARY KEY (people_id);

--relacion fact_table con country_dim
ALTER TABLE fact_table
    ADD CONSTRAINT fk_people
        FOREIGN KEY (people_id) REFERENCES people_dim(people_id);

-- Establecer country_id como llave primaria en country_dim
ALTER TABLE title_dim
    ADD CONSTRAINT pk_title PRIMARY KEY (title_id);

--relacion fact_table con country_dim
ALTER TABLE fact_table
    ADD CONSTRAINT fk_title
        FOREIGN KEY (title_id) REFERENCES title_dim(title_id);

-- Establecer country_id como llave primaria en country_dim
ALTER TABLE type_dim
    ADD CONSTRAINT pk_type PRIMARY KEY (type_id);

--relacion fact_table con country_dim
ALTER TABLE fact_table
    ADD CONSTRAINT fk_type
        FOREIGN KEY (type_id) REFERENCES type_dim(type_id);