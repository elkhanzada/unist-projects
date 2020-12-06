package hw3

import scala.collection.immutable.HashMap 
import hw3._


package object hw3 {
  type Env = HashMap[Var,Val]
  type Loc = Int
  
}

case class Mem(m: HashMap[Loc,Val], top: Loc) {
  def exists(v: Val): Boolean =
    m.exists((a: (Loc, Val)) => a._2 == v)
  def add(v: Loc, value: Val) = Mem(m + (v -> value),v)
}

sealed trait Val
case class IntVal(n: Int) extends Val
case class BoolVal(b: Boolean) extends Val
case class ProcVal(v: Var, expr: Expr, env: Env) extends Val
case class RecProcVal(fv: Var, av: Var, body: Expr, env: Env) extends Val
case class LocVal(l: Loc) extends Val


sealed trait Program
sealed trait Expr extends Program
case class Const(n: Int) extends Expr
case class Var(s: String) extends Expr
case class Add(l: Expr, r: Expr) extends Expr
case class Sub(l: Expr, r: Expr) extends Expr
case class Mul(l: Expr, r: Expr) extends Expr
case class Div(l: Expr, r: Expr) extends Expr
case class GTExpr(l: Expr, r: Expr) extends Expr
case class GEQExpr(l: Expr, r: Expr) extends Expr
case class Iszero(c: Expr) extends Expr
case class Ite(c: Expr, t: Expr, f: Expr) extends Expr
case class ValExpr(name: Var, value: Expr, body: Expr) extends Expr
case class VarExpr(name: Var, value: Expr, body: Expr) extends Expr
case class Proc(v: Var, expr: Expr) extends Expr
case class DefExpr(fname: Var, aname: Var, fbody: Expr, ibody: Expr) extends Expr
case class Asn(v: Var, e: Expr) extends Expr
case class Paren(expr: Expr) extends Expr
case class Block(f: Expr, s: Expr) extends Expr
case class PCall(ftn: Expr, arg: Expr) extends Expr







object MiniScalaInterpreter {

  case class UndefinedSemantics(msg: String = "", cause: Throwable = None.orNull) extends Exception("Undefined Semantics: " ++ msg, cause)


  def forEval(env: Env, mem: Mem, expr: Expr): (Mem, Val) = expr match {
    case Const(n) => (mem, IntVal(n))
    case Var(s) =>
      if (env.exists((a: (Var, Val)) => a._1 == Var(s))) {
        val temp = env(Var(s))
        temp match {
          case LocVal(l) => (mem,mem.m.getOrElse(l,throw UndefinedSemantics("Problem")))
          case _=> (mem,temp)
        }
      } else throw UndefinedSemantics("1")
    case Add(a,b) => (forEval(env,mem,a)._2, forEval(env,mem,b)._2) match {
      case (x: IntVal, y: IntVal)=> {
        val temp1 = mem.add(mem.top+1,x)
        val temp2 = mem.add(temp1.top+1,y)
        (temp2,IntVal(x.n+y.n))
      }
      case _ => throw UndefinedSemantics("Type Error")
    }
    case Sub(a,b) => (forEval(env,mem,a)._2, forEval(env,mem,b)._2) match {
      case (x: IntVal, y: IntVal) => {
        val temp1 = mem.add(mem.top+1,x)
        val temp2 = mem.add(temp1.top+1,y)
        (temp2,IntVal(x.n-y.n))
      }
      case _ => throw UndefinedSemantics("Type Error")
    }
    case Mul(a,b) => (forEval(env,mem,a)._2, forEval(env,mem,b)._2) match {
      case (x: IntVal, y: IntVal) => {
        val temp1 = mem.add(mem.top+1,x)
        val temp2 = mem.add(temp1.top+1,y)
        (temp2,IntVal(x.n*y.n))
      }
      case _ => throw UndefinedSemantics("Type Error")
    }
    case Div(a,b) => (forEval(env,mem,a)._2, forEval(env,mem,b)._2) match {
      case (x: IntVal, y: IntVal) => {
        val temp1 = mem.add(mem.top+1,x)
        val temp2 = mem.add(temp1.top+1,y)
        (temp2,IntVal(x.n/y.n))
      }
      case _ => throw UndefinedSemantics("Type Error")
    }
    case GTExpr(a,b) => (forEval(env,mem,a)._2, forEval(env,mem,b)._2) match {
      case (x: IntVal, y: IntVal) =>{
        val temp1 = mem.add(mem.top+1,x)
        val temp2 = mem.add(temp1.top+1,y)
        (temp2,BoolVal(x.n>y.n))
      }
      case _ => throw UndefinedSemantics("Type Error")
    }
    case GEQExpr(a,b) => (forEval(env,mem,a)._2, forEval(env,mem,b)._2) match {
      case (x: IntVal, y: IntVal) => {
        val temp1 = mem.add(mem.top+1,x)
        val temp2 = mem.add(temp1.top+1,y)
        (temp2,BoolVal(x.n >= y.n))
      }
      case _ => throw UndefinedSemantics("Type Error")
    }
    case Iszero(c) => forEval(env,mem,c)._2 match {
      case (x: IntVal) => {
        val temp1 = mem.add(mem.top+1,x)
        (temp1,BoolVal(x.n == 0))
      }
      case _ => throw UndefinedSemantics("Type Error")
    }
    case Ite(c, t, f) => forEval(env,mem,c)._2 match {
      case v: BoolVal => {
        val temp1 = mem.add(mem.top + 1, v)
        if (v.b) forEval(env, temp1, t)
        else forEval(env,temp1,f)
      }
      case _ => throw UndefinedSemantics("Type Error")
    }
    case Block(f, s) => {
      val temp1 = forEval(env,mem,f)
      forEval(env,temp1._1,s)
    }
    case Asn(v,e) =>{
      val temp2 = forEval(env,mem,e)._2
      v match {
        case Var(s) => {
          if(env.exists((a: (Var, Val)) => a._1 == Var(s))) {
            env(Var(s)) match {
              case LocVal(l) => {
                val temp3 = mem.add(l, temp2)
                (temp3, temp2)
              }
              case _ => throw UndefinedSemantics("Reassignment to Val")
            }
          }else{
            throw UndefinedSemantics("No such variable")
          }

        }
      }
      }
    case ValExpr(name, value, body) => {
      val temp1 = forEval(env,mem,value)
      val new_env = env + (name -> forEval(env,mem,value)._2)
      forEval(new_env, temp1._1, body)
    }
    case VarExpr(name, value, body) => {
      val temp1 = forEval(env,mem,value)
      val temp2 = mem.add(mem.top+1,temp1._2)
      val new_env = env + (name -> LocVal(temp2.top))
      forEval(new_env, temp2, body)
    }
    case Paren(expr: Expr) => forEval(env,mem,expr)

    case Proc(v,expr) => {
      (mem,ProcVal(v,expr,env))
    }

    case DefExpr(fname,aname,fbody,ibody) => {
      val recprocval = RecProcVal(fname, aname, fbody, env)
      val temp = env + (fname -> recprocval)
      val tempmem = mem.add(mem.top+1, recprocval)
      forEval(temp,tempmem, ibody)
    }
    case PCall(ftn,expr)  => (forEval(env,mem,ftn)._2) match {
      case (x: ProcVal) => {
        val tempmem = mem.add(mem.top+1,x)
        val args = forEval(env,tempmem,expr)._2
        val tempmem2 = tempmem.add(tempmem.top+1,args)
        val temp = x.env + (x.v -> args)
        forEval(temp,tempmem2,x.expr)
      }
      case (x: RecProcVal) => {
        val tempmem = mem.add(mem.top+1,x)
        val args = forEval(env,tempmem,expr)._2
        val tempmem2 = tempmem.add(tempmem.top+1,args)
        val temp2 = x.env + (x.av -> args) + (x.fv -> x)
        forEval(temp2,tempmem2,x.body)
      }
      case _ => throw UndefinedSemantics("Type Error")
    }
    case _ => throw UndefinedSemantics("Not Defined")
  }

  def doInterpret(env: Env, mem: Mem, expr: Expr): Val ={
    forEval(env,mem,expr)._2
  }
  
  def apply(program: String): Val = {
    val parsed = MiniScalaParserDriver(program)
    doInterpret(new Env(), Mem(new HashMap[Loc,Val],0), parsed)
  }

}


object Hw3App extends App {
  
//  println(MiniScalaInterpreter("{def f(x) = if iszero x then 0 else x + (f x-1) ; f 1}"))
  println(MiniScalaInterpreter("{def sq(x) = y := x * x; {var y = 3; (sq y)}}"))

}
