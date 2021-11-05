CREATE TABLE hazel_martinez2(
	id SERIAL PRIMARY KEY NOT NULL,
	campo1 CHAR(50) NOT NULL,
	hijos INT NULL
);

CREATE TABLE student(
	id SERIAL PRIMseARY KEY NOT NULL,
	name VARCHAR(100) NOT NULL,
	phone VARCHAR(1000) NULL,
	grade INT NOT NULL,
	teacher_id INT,
	CONSTRAINT fk_teacher
    	FOREIGN KEY(teacher_id) 
	  		REFERENCES teacher(id)
	  			ON DELETE CASCADE
	  			ON UPDATE NO ACTION
);
INSERT INTO student (name, phone, grade, teacher_id) VALUES 
('Aaron' , '+5533557733', 6, 1),
('Mustafa' , '+5533557733', 5, 2),
('Ygvil' , '+5533557733', 4, 3),
('Olga', '+5544009944', 6, 4),
('Aaron' , '+5533557733', 6, 5),
('Mustafa' , '+5533557733', 5, 6),
('Ygvil' , '+5533557733', 4, 7),
('Olga', '+5544009944', 6, 8);


CREATE TABLE teacher(
	id SERIAL PRIMARY KEY NOT NULL,
	name VARCHAR(100) NOT NULL,
	subject VARCHAR(100) NOT NULL,
	phone VARCHAR(1000) NULL,
	salary DECIMAL NOT NULL
);


CREATE TABLE phone(
	id SERIAL PRIMARY KEY NOT NULL,
	number VARCHAR(14) NOT NULL,
	teacher_id INT NOT NULL,
	CONSTRAINT fk_teacher_phone
    	FOREIGN KEY(teacher_id) 
	  		REFERENCES teacher(id)
	  			ON DELETE CASCADE
	  			ON UPDATE NO ACTION
);

INSERT INTO phone (number, teacher_id) VALUES
('+5215533773377', 1),
('+5215599009900', 1);

INSERT INTO teacher (name, subject, phone, salary) VALUES
('Hazel', 'Systems', '+553377557733 +5577337733', 20000),
('Fernando', 'Spanish', '+553377557733', 10000),
('Alejandro', 'Math', '+553377557733', 25000),
('Maria', 'Art', '+553377557733', 17000),
('Manuel', 'Sports', '+5566776677', 13000),
('Hazel', 'Systems', '+553377557733 +5577337733', 20000),
('Fernando', 'Spanish', '+553377557733', 10000),
('Alejandro', 'Math', '+553377557733', 25000),
('Maria', 'Art', '+553377557733', 17000),
('Manuel', 'Sports', '+5566776677', 13000);

INSERT INTO hazel_martinez (campo1, hijos) VALUES ('campo1',0);

SELECT * FROM hazel_martinez;

INSERT INTO hazel_martinez VALUES (2, 'campo2', 1);
INSERT INTO hazel_martinez2 (campo1) VALUES ('campo4');

ALTER SEQUENCE hazel_martinez2_id_seq RESTART WITH 3;
SELECT setval('hazel_martinez', 2);

DELETE FROM hazel_martinez WHERE id=2;

INSERT INTO hazel_martinez2 (campo1, hijos) SELECT campo1, hijos FROM hazel_martinez;

UPDATE hazel_martinez SET campo1 ='campo', hijos =3 WHERE hijos = 2; 

INSERT INTO hazel_martinez2 (campo1, hijos) SELECT campo1, hijos FROM hazel_martinez;

SELECT AVG(hijos) FROM hazel_martinez2;


SELECT * FROM student AS s
INNER JOIN teacher AS t
ON s.teacher_id = t.id


SELECT name, phone FROM student UNION SELECT name, phone FROM teacher;