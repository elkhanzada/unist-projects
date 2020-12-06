class Hw1Test extends org.scalatest.funsuite.AnyFunSuite {
  test("Hw1.fibo") {
    assert(Hw1.fibo(1) === 1)
    assert(Hw1.fibo(9) === 55)
    assert(Hw1.fibo(10) === 89)
    assert(Hw1.fibo(11) === 144)
    assert(Hw1.fibo(12) === 233)
    assert(Hw1.fibo(13) === 377)
    assert(Hw1.fibo(14) === 610)


  }

  test("Hw1.sum") {
    def constant(x: Int) = x
    def square(x: Int) = x * x
    def cube(x: Int) = x*x*x
    assert(Hw1.sum(constant,10) === 55)
    assert(Hw1.sum(square,2) === 5)
    assert(Hw1.sum(cube,5) === 225)

  }

  test("Hw1.foldRight") {
    assert(Hw1.foldRight(100, (x: Int, y:Int) => x % y, Cons(5,Cons(3,Nil))) === 1)
    assert(Hw1.foldRight(100, (x: Int, y:Int) => x % y, Cons(3,Cons(5,Nil))) === 0)
    assert(Hw1.foldRight(100, (x: Int, y:Int) => x % y, Cons(6,Cons(25,Cons(55,Nil)))) === 2)
    assert(Hw1.foldRight(100, (x: Int, y:Int) => x % y, Cons(25,Cons(6,Cons(55,Nil)))) === 3)
    assert(Hw1.foldRight(100, (x: Int, y:Int) => x % y, Cons(7,Cons(12,Cons(39,Cons(200, Cons(400, Nil)))))) === 3)
    assert(Hw1.foldRight(2339, (x: Int, y:Int) => x % y, Cons(7,Cons(12,Cons(39,Cons(200, Cons(400, Nil)))))) === 3)
    assert(Hw1.foldRight(2339, (x: Int, y:Int) => x % y, Cons(39,Cons(12,Cons(7,Cons(200, Cons(400, Nil)))))) === 6)

  }

  test("Hw1.filter") {
    assert(Hw1.filter((x: Int) => x % 3 == 0, Cons(5,Cons(3,Cons(6,Nil)))) === Cons(3,Cons(6,Nil)))
    assert(Hw1.filter((x: Int) => x % 5 == 0, Cons(5,Cons(3,Cons(6,Nil)))) === Cons(5,Nil))
    assert(Hw1.filter((x: Int) => x % 2 == 0, Cons(12,Cons(5,Cons(3,Cons(6,Cons(25,Cons(22,Cons(15,Cons(11,Nil))))))))) === Cons(12,Cons(6,Cons(22,Nil))))
    assert(Hw1.filter((x: Int) => x % 2 == 0, Cons(12,Cons(8,Cons(4,Cons(6,Cons(28,Cons(22,Cons(16,Cons(12,Nil))))))))) === Cons(12,Cons(8,Cons(4,Cons(6,Cons(28,Cons(22,Cons(16,Cons(12,Nil)))))))))

  }

  test("Hw1.iter") {
    def constant(x: Int) = x
    def square(x: Int) = x * x
    def mult(x: Int) = 3*x
    assert(Hw1.iter[Int](constant, 10)(10) === 10)
    assert(Hw1.iter[Int](square, 3)(2) === 256)
    assert(Hw1.iter[Int](mult, 5)(5) === 1215)
  }

  test("Hw1.insert") {
    val step_0 = IntNode(10,IntNode(9,IntNode(8,Leaf,Leaf),Leaf),Leaf)
    val step_1 = Hw1.insert(step_0, 11)
    val step_2 = Hw1.insert(step_1, 12)
    val step_3 = Hw1.insert(step_2,7)
    assert(step_1 === IntNode(10,IntNode(9,IntNode(8,Leaf,Leaf),Leaf),IntNode(11,Leaf,Leaf)))
    assert(step_2 === IntNode(10,IntNode(9,IntNode(8,Leaf,Leaf),Leaf),IntNode(11,Leaf,IntNode(12,Leaf,Leaf))))
    assert(step_3 === IntNode(10,IntNode(9,IntNode(8,IntNode(7,Leaf,Leaf),Leaf),Leaf),IntNode(11,Leaf,IntNode(12,Leaf,Leaf))))

  }

  test("Hw1.eval") {
    assert(Hw1.eval(True) === true)
    assert(Hw1.eval(Andalso(Orelse(True,False),True)) === true)
    assert(Hw1.eval(Implies(Andalso(True,Orelse(True,False)),False)) === false)

  }


}
