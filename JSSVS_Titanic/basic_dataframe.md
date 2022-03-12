## pandas

데이터 분석을 위한 파이썬 라이브러리

행과 열로 이루어진 데이터 구조를 다룬다.

Series 와 Dataframe 자료구조를 사용한다.

## Dataframe 생성

```python
import pandas as pd

#테스트 데이터 dict 생성
data_exam = {
    'name':['a','b','c','d','e'],
    'height':[160,170,180,185,190],
    'age':[23,15,18,19,25],
    'class':['A','B','A','B','A']
}
.
#pandas dataframe 
df=pd.DataFrame(data_exam)

#read from csv file
df=pandas.read_csv(filepath,names=cols,header=None,encoding="cp949")

#Dataframe()으로 호출하면 안되니까 타이핑에 주의하자

df.index
df.columns
df.dtypes
```

## Dataframe 다루기

```python
> 특정 컬럼 조회
df['id'] 

> 특정 복수 컬럼 조회.
df[['id','age']] 

> where 절 조건 조회

df[('id'>10)] # ID 10이상만 조회

df.where(filter1 & filter2, inplace = True)

>컬럼 이름 변경
df.rename(columns={'oldName':'newName'},inplace=True)

>Dataframe convert to tuple
tmp = df['id']
mytuple = [x for x in tmp.to_numpy()]

> 특정 조건 필터
df [ 조건 ]

> 컬럭 삭제
df.drop(['컬럼이름','col2'],axis=1)

> 데이터 값 변경
df['Gender'].replace('male',1) # Gender 컬럼의 male 값을 1로 대체

```

## where, query

```sql
dt.where(dt.컬럼명1 == 'value').count()['id']

dt.query('컬럼명1 == "value" | 컬럼명2 > 5').count()
```

## group by

```python
dt.groupby('class') #집계할 컬럼
.agg({'height':['count','mean']}) #집계 함수를 적용
.sort_values([('height','mean')]) # 정렬

#agg 에 컬럼 이름을 주면 multiIndex로 생성되는데 () set 형태로 컬럼 이름이 생성된다.

dt.groupby('컬럼이름').size()  그룹별 카운트
```

## dataframe join

```python
merge_view=view.merge(user,on='uid').merge(product,on='pid')
merge_view=view.merge(user,on='uid').merge(product,on='pid',how='outer')

```

### new DataFrame

```sql
columns=["appid","detect_time","header_cnt","worker_cnt","fraud_buyer_cnt","ymd"]
new_row = [('443410','2021-06-23 10:00:00',header_cnt,worker_cnt,fraud_buyer_cnt,'2021-09-16')]

hist_dataframe = pd.DataFrame(new_row,columns=columns)
```

### parquet 로 부터 데이터 읽기

```python
from fastparquet import ParquetFile

# 만약 압축을 풀어야 한다면
import snappy
def snappy_decompress(data, uncompressed_size):
    return snappy.decompress(data)

pf = ParquetFile('sample.snappy.parquet') # filename includes .snappy.parquet extension
df=pf.to_pandas()
```

### MySQL 에서 데이터 읽기

```sql
from sqlalchemy import create_engine
import pandas as pd
import pymysql

db_conn_str = 'mysql+pymysql://biuser:Biuser%!$!@mig-test.cluster-csmfl3dv6qto.ap-northeast-2.rds.amazonaws.com/kars_dev1'
mysql_conn = create_engine(db_conn_str)

data = pd.read_sql_table('BOT_USER',mysql_conn)
```

### DataFrame API

DF.info()

- DF의 스키마 정보보기
- DF.info(show_counts=True)

DF.set_index()

- DF 내 열(컬럼)을 이용하여 인덱스를 설정한다
- DF.set_index(keys, drop=True, append=False, inplace = False)

DF.iloc (integer location)

- DF 의 행이나 컬럼의 순서를 나타낸느 정수로 특정 값을 추출해온다.
- DF.iloc[행 인덱스, 열 인덱스]
    
    ex)
    
    ```python
    df.iloc[::2,:]
    df 전체 값중 짝수번째 행만 추출하고, 열은 전체 추출해라
     
    df.iloc[-10:]
    df 전체 값 중 인덱스 기준으로 끝에서 10개만 추출
    ```
    

DF.astype()

- 데이터 프레임의 타입 변경
- df.astype({’컬럼명’: ‘type’})

```python
DF.index[0].datetime64[s]
int64 -> datetime64 seconds 

df = df.astype({ ‘col1’: ‘str’}) 
```

DF.dtypes()

- 데이터 프레임 타입 확인하기

DF.isnull().sum()

- 컬럼별 널값 개수 구하기

DF.dropna(axis=0/1 , how = ‘any/all’, subset = [col1], inplace =True/False)

- axis
    - 0 = index = Nan 값이 포함된 행을 drop
    - 1 = column = Nan 값이 포함된 컬럼을 drop
- how
    - all = row 또는 column 에 있는 모든 값이 Nan 이어야 drop
- inplace
    - True = Dropna 를 DF 원본에 적용
    - False= Dropna 의 카피본 Dataframe 을 반환
- subset
    - 명시하지 않으면 DF 전체 적용
    - 명시한 컬럼만 dropna 진행