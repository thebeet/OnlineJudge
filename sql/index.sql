ALTER TABLE `newoj`.`solution`
ADD INDEX `result_date` (`result` ASC, `submit_time` ASC) ;

ALTER TABLE `newoj`.`user_problem`
ADD UNIQUE INDEX `user_problem` (`user_id` ASC, `problem_id` ASC) 
, ADD INDEX `result_user_problem` (`result` ASC, `user_id` ASC, `problem_id` ASC)
, ADD INDEX `result_problem` (`result` ASC, `problem_id` ASC)
, ADD INDEX `collect_user` (`collect` ASC, `user_id` ASC) ;

ALTER TABLE `newoj`.`user`
ADD INDEX `rank` (`solved` DESC, `last_solve_time` ASC) ;

ALTER TABLE `newoj`.`solution`
ADD INDEX `result_user` (`result` ASC, `user_id` ASC)
, ADD INDEX `result_user_problem_language` (`result` ASC, `user_id` ASC, `problem_id` ASC, `language_id` ASC) 
, ADD INDEX `problem_rank` (`problem_id` ASC, `result` ASC, `user_id` ASC, `run_time` ASC, `memory` ASC, `submit_time` ASC) ;

ALTER TABLE `newoj`.`contest_user_problem`
ADD UNIQUE INDEX `contest_user_problem` (`contest_id` ASC, `user_id` ASC, `problem_id` ASC);
