from lox import expr 
from lox import stmt 



class Printer(expr.Visitor[str], stmt.Visitor[str]):

    def visit_binary_expression(self, e : expr.Binary) -> str: 
        return f"({e.operator.value} {e.left.accept(self)} {e.right.accept(self)})" 

    def visit_grouping_expression(self, e : expr.Grouping) -> str:
        return f"('group', {e.expression.accept(self)})" 

    def visit_literal_expression(self, e : expr.Literal) -> str:
        return f"({e.value})"   

    def visit_unary_expression(self, e : expr.Unary) -> str:
        return f"({e.operator.value} {e.right.accept(self)})"   
    
    def visit_expression_statement(self, s : stmt.Expression):
        return f"[Statement : {s.expression.accept(Printer)}]"
    
    def visit_print_statement(self, s : stmt.Print):
        return f"[Statement : print {s.expression.accept(Printer)}]"
    
    def visit_variable_statement(self, s : stmt.Var):
        return f"[Statement: var {s.name.value, s.initializer.accept(Printer)}]"