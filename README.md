## 1. 프로젝트 소개

### 딥러닝 기반 워크로드 분석을 통한 SSD 성능 개선

### 목적
딥러닝 기반 워크로드 분석을 통하여 SSD의 쓰기/삭제 단위가 다르며, 덮어쓰기 할 수 없는 성질로 인한 성능 저하 개선

### 개요
SSD(Solid State Drive)는 NAND 플래시 메모리로 구성되어 있어 데이터에 대한 덮어쓰기가 불가하며 쓰기와 삭제의 단위가 다르기 때문에 성능 저하가 발생할 수 있다. 
데이터를 덮어쓰기(수정하기) 위해서는 쓰기 전에 삭제(Erase Before Write) 작업이 필수적이다. 이 때, 읽기와 쓰기는 페이지(Page) 단위로 실행되며, 삭제는 블록(Block) 단위로 실행되기 때문에 문제가 발생한다.
이미 쓰기가 수행된 페이지에 새로운 쓰기가 수행된다면, 기존 페이지는 Invalid 상태가 되고, 쓰기는 블록 내 비어있는 페이지에 진행된다. 
이 때 비어있는 페이지의 수가 임계치(Garbage Collection Trigger) 이하로 적어졌다면 가비지 컬렉션(Garbage Collection)이 수행된다. 
가비지 컬렉션은 블록에 있는 모든 Valid 데이터들을 다른 비어있는 블록에 쓰고, 블록의 모든 페이지를 지워 해당 블록을 Empty 상태로 만드는 과정이다. 
다른 비어있는 블록에 쓰는 과정에서 추가적인 쓰기가 발생되고, 이는 추가적인 수행 시간을 요한다. 
위와 같은 이유로, 자주 변경되는 데이터를 Hot, 자주 변경되지 않는 데이터를 Cold로 분류하여 SSD 내부에서의 데이터 배치를 최적화한다.
분류된 데이터를 서로 다른 블록으로 분리함으로써 전체 쓰기 증폭을 줄이며, GC가 더 효율적으로 동작하도록 할 수 있다.
최종적으로, 데이터를 분류하는 시뮬레이션과, 데이터를 분류하지 않는 시뮬레이션의 결과를 비교한다.

## 2. 팀 소개

#### 공희찬 (201724409)
- Email: sk980919@naver.com
- 학습 데이터 전처리 및 레이블링
- 모델 개발
- 시뮬레이터 제작
- 시뮬레이터 성능 테스트 및 WA 개선을 위한 파라미터 튜닝
- 포스터 및 보고서 작성

#### 박선민 (201824472)
- Email: john8981656@naver.com
- 모델 튜닝
- 포스터 및 보고서 작성

#### 박영훈 (201824476)
- Email: pyh007264@gmail.com
- 데이터 레이블링
- 모델 튜닝
- 보고서 작성

## 3. 구성도

### 연구 목표
![https://user-images.githubusercontent.com/64733547/278001532-4ed7c42e-2c05-4d7a-90da-a50e2209e92c.png](https://user-images.githubusercontent.com/64733547/278001532-4ed7c42e-2c05-4d7a-90da-a50e2209e92c.png)

### 모델 구조
![https://user-images.githubusercontent.com/64733547/278001512-f82162ee-c4ea-4236-9c47-96cfc9fa836d.png](https://user-images.githubusercontent.com/64733547/278001512-f82162ee-c4ea-4236-9c47-96cfc9fa836d.png)

### 시뮬레이터 Flow Chart
![https://user-images.githubusercontent.com/64733547/278001483-ba152b62-fa51-4779-ada7-8d485117776a.png](https://user-images.githubusercontent.com/64733547/278001483-ba152b62-fa51-4779-ada7-8d485117776a.png)

### 실험 결과

![](https://user-images.githubusercontent.com/64733547/278003446-df43e21a-1cec-4258-b827-4f3d1723974b.png)
- Write Amplification 2.1% 감소

![](https://user-images.githubusercontent.com/64733547/278003199-d6de53f1-c13e-4125-95a2-d2781765a8ec.png)
- 쓰기 요청이 증가할수록 쓰기 증폭 감소
- 기계학습으로 워크로드를 분석하여 데이터를 분류함으로써 쓰기 증폭을 감소시켰음

## 4. 소개 및 시연 영상

- TBD

## 5. 사용법

### Requirements

- python 3.8.5
- [I/O Trace csv file](https://traces.cs.umass.edu/index.php/Storage/Storage)
  - `csv/raw`에 `Financial1.csv` 추가
```
$ pip install numpy
$ pip install pandas
$ pip install tensorflow
```

### 코드
- `src` 폴더의 숫자 순서대로 .ipynb 파일을 실행하며 csv 파일을 생성
- `simulator/withML`
  - `config.py` 에서 각 파라미터 설정
  - `model` 폴더에 생성한 모델이 있는지 확인
  - `main.py` 실행
- `simulator/withoutML`
  - `config.py`에서 각 파라미터 설정
  - `main.py` 실행