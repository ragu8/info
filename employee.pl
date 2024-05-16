% Employee data
employee(john, engineering).
employee(susan, engineering).
employee(michael, marketing).
employee(emma, marketing).
employee(alex, finance).
employee(lisa, finance).
employee(jake, finance).
employee(james, sales).
employee(sarah, sales).

% Rule for defining manager-subordinate relationship
manager(john, susan).  % John is the manager of Susan
manager(michael, emma). % Michael is the manager of Emma
manager(alex, lisa).   % Alex is the manager of Lisa
manager(alex, jake).   % Alex is the manager of Jake
manager(james, sarah). % James is the manager of Sarah

% Rule for defining colleague relationship
colleague(X, Y) :- employee(X, Department), employee(Y, Department), X \= Y.

% Rule for defining team members based on the same manager
team_member(X, Y) :- manager(Y, X).
team_member(X, Y) :- manager(X, Y).

% Rule for defining department members based on the same department
department_member(X, Y) :- employee(X, Department), employee(Y, Department), X \= Y.

% Rule for defining all team members recursively
all_team_members(X, Y) :- team_member(X, Y).
all_team_members(X, Y) :- team_member(X, Z), all_team_members(Z, Y).

% Rule for defining all department members recursively
all_department_members(X, Y) :- department_member(X, Y).
all_department_members(X, Y) :- department_member(X, Z), all_department_members(Z, Y).

% Queries
% 1. Who are the team members of John?
all_team_members(john, X).

% 2. Who are the colleagues of Susan?
colleague(susan, X).

% 3. Who is the manager of Emma?
manager(X, emma).

% 4. Who are the team members of Alex?
all_team_members(alex, X).

% 5. Who are the colleagues of James?
colleague(james, X).

% 6. Who are the department members of Finance?
all_department_members(X, finance).

% 7. Is Susan a colleague of James?
colleague(susan, james).

% 8. Is Michael a manager of Sarah?
manager(michael, sarah).

