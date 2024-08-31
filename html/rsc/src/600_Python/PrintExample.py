# 문자열, 숫자 등의 다양한 데이터를 출력

# 문자열 출력
print( "Hello, World!" )
# 정수 출력
print(123)
# 실수 출력
print(4.56)


# 다양한 변수 데이터 출력
# 문자열 변수 출력
a = "Hello, World!"
print( a )
# 정수 변수 출력
b = 123
print( b )
# 실수 변수 출력
c = 4.56
print( c )

# 쉼표(,)로 구분된 여러 값들은
# 스페이스 문자로 구분하여 출력합니다.
print( "Hello", "World", 123 )

# 구분 문자(sep)를 지정할 수 있습니다.
print( "Hello", "World", 123, sep=' ' )
# 여러가지 구분 문자를 사용할 수 있습니다.
print( "Hello", "World", 123, sep='*' )
print( "Hello", "World", 123, sep='#' )

# 출력 후 줄 바꿈(=개행)을 합니다. 
print( "Hello" )
print( "World" )

# 줄 바꿈 문자(end)를 지정할 수 있습니다.
print("Hello", end="")
print("World")
print("Hello", "World")

# 구분 문자(sep)와 줄 바꿈 문자(end)를 함께 지정합니다.
print( "Hello", "World", 123, sep="-", end="" )
print( 4.56 )

# 버퍼를 비우고 화면으로 출력합니다.
print( "Hello", end=" ", flush=True )
print( "World", 123 )

# 데이터를 파일로 출력합니다.
textFile = open("text.txt", "w")
print("Hello", "World!", 123, file=textFile)