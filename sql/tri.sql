-- Trigger DDL Statements
DELIMITER $$

USE `newoj`$$

CREATE
DEFINER=`root`@`localhost`
TRIGGER `newoj`.`solution_insert`
AFTER INSERT ON `newoj`.`solution`
FOR EACH ROW
begin
    insert into user_problem(user_id, problem_id, result, collect) values (new.user_id, new.problem_id, new.result, 0)
        on duplicate key update result=if(result=1, result, new.result);
    if (new.contest_id is not null) then
        if exists(select id from solution
            where contest_id=new.contest_id and user_id=new.user_id and problem_id=new.problem_id and result=1 order by id limit 1) then
            begin
                DECLARE	mid int;
                DECLARE first_solve_time timestamp;
                set mid = (
                    select id from solution
                    where contest_id=new.contest_id and user_id=new.user_id and problem_id=new.problem_id and result=1 order by id limit 1
                    );
                set first_solve_time = (
                    select submit_time from solution
                    where contest_id=new.contest_id and user_id=new.user_id and problem_id=new.problem_id and result=1 order by id limit 1
                    );
                insert into contest_user_problem(contest_id, user_id, problem_id, result, penatly, solve_time)
                    values (new.contest_id, new.user_id, new.problem_id, new.result, if(new.result=1,0,1200), first_solve_time)
                    on duplicate key update result=1, penatly=1200*(select count(*) from solution
                        where contest_id=new.contest_id and user_id=new.user_id and problem_id=new.problem_id and id<mid), solve_time=first_solve_time;
            end;
        else
            insert into contest_user_problem(contest_id, user_id, problem_id, result, penatly, solve_time)
                values (new.contest_id, new.user_id, new.problem_id, new.result, if(new.result=1,0,1200), null)
                on duplicate key update result=new.result, penatly=1200*(select count(*) from solution
                    where contest_id=new.contest_id and user_id=new.user_id and problem_id=new.problem_id), solve_time=null;
        end if;
    end if;
end$$

CREATE
DEFINER=`root`@`localhost`
TRIGGER `newoj`.`solution_update`
AFTER UPDATE ON `newoj`.`solution`
FOR EACH ROW
begin
    update user_problem set result=if(result=1,1,new.result) where user_id = new.user_id and problem_id = new.problem_id;
    if (new.contest_id is not null) then
        if exists(select id from solution
            where contest_id=new.contest_id and user_id=new.user_id and problem_id=new.problem_id and result=1 order by id limit 1) then
            begin
                DECLARE	mid int;
                DECLARE first_solve_time timestamp;
                set mid = (
                    select id from solution
                    where contest_id=new.contest_id and user_id=new.user_id and problem_id=new.problem_id and result=1 order by id limit 1
                    );
                set first_solve_time = (
                    select submit_time from solution
                    where contest_id=new.contest_id and user_id=new.user_id and problem_id=new.problem_id and result=1 order by id limit 1
                    );
                insert into contest_user_problem(contest_id, user_id, problem_id, result, penatly, solve_time)
                values (new.contest_id, new.user_id, new.problem_id, new.result, if(new.result=1,0,1200), first_solve_time)
                on duplicate key update result=1, penatly=1200*(select count(*) from solution
                    where contest_id=new.contest_id and user_id=new.user_id and problem_id=new.problem_id and id<mid), solve_time=first_solve_time;
            end;
        else
            insert into contest_user_problem(contest_id, user_id, problem_id, result, penatly, solve_time)
                values (new.contest_id, new.user_id, new.problem_id, new.result, if(new.result=1,0,1200), null)
                on duplicate key update result=new.result, penatly=1200*(select count(*) from solution
                    where contest_id=new.contest_id and user_id=new.user_id and problem_id=new.problem_id), solve_time=null;
        end if;
    end if;
end$$

CREATE
DEFINER=`root`@`localhost`
TRIGGER `newoj`.`user_problem_insert`
AFTER INSERT ON `newoj`.`user_problem`
FOR EACH ROW
begin
    update user set solved = solved + if(new.result=1,1,0) where user_id = new.user_id;
    update problem set solved = solved + if(new.result=1,1,0) where id = new.problem_id;
end$$
CREATE
DEFINER=`root`@`localhost`
TRIGGER `newoj`.`user_problem_update`
AFTER UPDATE ON `newoj`.`user_problem`
FOR EACH ROW
begin
    update user set solved = solved - if(old.result=1,1,0) + if(new.result=1,1,0) where user_id = old.user_id;
    update problem set solved = solved - if(old.result=1,1,0) + if(new.result=1,1,0) where id = old.problem_id;
end$$


