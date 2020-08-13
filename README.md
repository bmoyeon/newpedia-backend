# newpedia-backend

## Introduction
- wecode 9기 수강생들의 3차 프로젝트입니다.
- 프로젝트 기간 : 2020.7.20 ~ 2020.8.14 (4주)
- 2명의 개발자가 함께 협업했습니다. (1 Front-End, 1 Back-End)

## 3차 프로젝트 소개
 새로이 탄생하는 신조어를 검색하고 직접 등록 할 수 있는 신조어 오픈사전, 뉴피디아 사이트 제작
 
## modeling
<img src="https://user-images.githubusercontent.com/60872814/90104175-c2151200-dd7e-11ea-81a9-5842a965635b.png"></img>

## Goal
- 카카오소셜로그인 기능 구현하기
- Back-End API를 통해 데이터를 GET / POST / PUT 하기
- 단어 등록 및 수정
- trello를 사용해 협업하며 매일 정해진 시간에 stand up 미팅 진행하기

## Technologies
- Python: List-complihension, Generator Expression
- Django: select_related, prefetch_related, ORM, paginator
- Postman: api 문서화
- RESTful API
- unit test
- AWS, Docker
- Git, GitHub

## Features
- 회원가입 및 로그인 (bcrypt와 jwt를 활용한 access_token 전송)
- 카카오톡 소셜 로그인
- 인가 기능 데코레이터
- 단어 등록 및 수정
- 단어리스트와 단어상세페이지 데이터 전송
- 페이지네이션 구현
- 단어 검색 기능 구현
- 각 엔드포인트에 대한 unit test 진행

## API Documentation
https://documenter.getpostman.com/view/11626571/T1DsAG1J?version=latest
