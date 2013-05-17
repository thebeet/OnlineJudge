insert newoj.auth_user 
   (select uid, username, "","",email,password,0,1,0,login_time,reg_time from oj.user);

INSERT INTO `newoj`.`user`
(`user_id`, `nickname`, `reg_ip`, `login_ip`, `school`, `institute`, `department`, `birthday`,
`gender`, `phone`, `address`, `realname`, `stu_no`, `solved`, `last_solve_time`)
(select uid, nickname, reg_ip, login_ip, school, institute, department, birthday,
sex, phone, address, realname, stu_no, 0, null from oj.user);

INSERT `newoj`.`problem`
(`id`, `title`, `case_number`, `time_limit`, `case_time_limit`, `memory_limit`, `output_limit`,
`is_spj`, `description`, `input`, `output`, `sample_input`, `sample_output`, `hint`, `source`, 
`analysis`, `create_time`, `defunct`, `solved`)
(select pid, title, case_number, time_limit, case_time_limit, memory_limit, output_limit,
        is_spj, description, input, output, sample_input, sample_output, hint, source,
        analysis, create_time, defunct, 0 from oj.problem);

INSERT INTO `newoj`.`judger` (`id`, `ip`, `port`, `judger_name`, `info`, `defunct`)
 VALUES (1, '127.0.0.1', 13146, 'XMU', 'none', 0);

insert newoj.language(id, name, defunct)
(select lid, language, 0 from oj.language );

INSERT INTO `newoj`.`contest`
(`id`, `title`, `description`, `start_time`, `end_time`, `type`, `defunct`)
(select cid, title, description, start_time, end_time, type, defunct from oj.contest);

INSERT INTO `newoj`.`user_problem`
(`user_id`,`problem_id`, `collect`)
(select uid, pid, 1 from oj.user_targets)
ON DUPLICATE KEY UPDATE collect=1;
#;

INSERT INTO `newoj`.`contest_problem`
(`contest_id`, `problem_id`,`display_order`)
(select `cid`, `pid`, `display_order` from oj.contest_problems );


INSERT INTO `newoj`.`solution`
(`id`, `user_id`, `problem_id`, `language_id`, `contest_id`, `submit_time`, `result`, `run_time`, `memory`,
`source_code`, `result_detail`, `judger_id`)
(select sid, uid, pid, lid, if(cid=-1, null, cid), submit_time, result, run_time, memory, 
    source_code, null, 1 from oj.problem_solution limit 1000);

INSERT INTO `newoj`.`solution`
(`id`, `user_id`, `problem_id`, `language_id`, `contest_id`, `submit_time`, `result`, `run_time`, `memory`,
`source_code`, `result_detail`, `judger_id`)
(select sid, uid, pid, lid, if(cid=-1, null, cid), submit_time, result, run_time, memory, 
    source_code, null, 1 from oj.problem_solution limit 1000,9000);

INSERT INTO `newoj`.`solution`
(`id`, `user_id`, `problem_id`, `language_id`, `contest_id`, `submit_time`, `result`, `run_time`, `memory`,
`source_code`, `result_detail`, `judger_id`)
(select sid, uid, pid, lid, if(cid=-1, null, cid), submit_time, result, run_time, memory, 
    source_code, null, 1 from oj.problem_solution limit 10000,40000);
    
INSERT INTO `newoj`.`solution`
(`id`, `user_id`, `problem_id`, `language_id`, `contest_id`, `submit_time`, `result`, `run_time`, `memory`,
`source_code`, `result_detail`, `judger_id`)
(select sid, uid, pid, lid, if(cid=-1, null, cid), submit_time, result, run_time, memory, 
    source_code, null, 1 from oj.problem_solution limit 50000,50000);
        
INSERT INTO `newoj`.`solution`
(`id`, `user_id`, `problem_id`, `language_id`, `contest_id`, `submit_time`, `result`, `run_time`, `memory`,
`source_code`, `result_detail`, `judger_id`)
(select sid, uid, pid, lid, if(cid=-1, null, cid), submit_time, result, run_time, memory, 
    source_code, null, 1 from oj.problem_solution limit 100000,50000);
            
INSERT INTO `newoj`.`solution`
(`id`, `user_id`, `problem_id`, `language_id`, `contest_id`, `submit_time`, `result`, `run_time`, `memory`,
`source_code`, `result_detail`, `judger_id`)
(select sid, uid, pid, lid, if(cid=-1, null, cid), submit_time, result, run_time, memory, 
    source_code, null, 1 from oj.problem_solution limit 150000,50000);
/*
insert newoj.user_problem (user_id, problem_id, result, solution_id)
(select uid, pid, ifnull(ac,0), solution from
    (select uid, pid from oj.problem_solution group by uid, pid) as t1 left join 
    (select uid, pid, 1 ac, min(sid) solution from oj.problem_solution where result=1 group by uid, pid) as t2
        using(uid, pid)
);

update newoj.user inner join 
    (select user_id, count(*) c from newoj.user_problem group by user_id) as t
    using (user_id) set  solved = c;
update newoj.problem inner join 
    (select problem_id id, count(*) c from newoj.user_problem group by problem_id) as t
    using (id) set solved = c;
*/
INSERT INTO `newoj`.`discuss`
(`id`, `problem_id`, `reply_id`, `user_id`, `title`, `content`, `create_time`, `edit_time`,
`reply_num`,`view_num`, `last_reply_user_id`, `last_reply_time`, `defunct`)
(select discuss_id, if(pid=0, null, pid), reply_id, uid, title, content, date, date,
reply_num, view_num, last_reply_uid, last_reply_date, defunct from oj.discuss);


INSERT INTO `newoj`.`mail`
(`id`, `from_user_id`, `to_user_id`, `title`, `content`, `create_time`, `view`,`defunct`)
(select mail_id, fromid, toid, title, content, date, new=0, defunct from oj.mail)