# 문자열, 숫자, 변수 등 다양한 데이터를 출력

# 문자열 출력
print("Hello, World!")

# 정수 출력
print(123)

# 실수 출력
print(4.56)

# 쉼표(,)로 구분된 여러 값들은
# 스페이스 문자로 구분하여 출력합니다.
print( "Hello", "World", 123, 4.56 )

# 구분 문자(sep)를 지정할 수 있습니다.
print( "Hello", "World", 123, 4.56, sep=' ' )
# 여러가지 구분문자를 사용할 수 있습니다.
print( "Hello", "World", 123, 4.56, sep='*' )
print( "Hello", "World", 123, 4.56, sep='#' )

# 출력 후 줄 바꿈(=개행)을 합니다. 
print("Hello")
print("World")

# 줄 바꿈 문자(end)를 지정할 수 있습니다.
print("Hello", end=" ")
print("World")
print("Hello", "World")

# f-string 메서드를 사용하여 출력 형식을 지정합니다.
name = "Alice"
print(f"Hello, {name}!")

# format() 메서드를 사용하여 출력 형식을 지정합니다.
name = "Alice"
print("Hello, {0}!".format( name ) )

