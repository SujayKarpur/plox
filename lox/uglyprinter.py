from lox.expr import Visitor, Binary, Grouping, Literal, Unary




class Printer(Visitor[str]):

    def visit_binary_expression(self, expr : Binary) -> str: 
        return f"({expr.operator.value} {expr.left.accept(self)} {expr.right.accept(self)})" 

    def visit_grouping_expression(self, expr : Grouping) -> str:
        return f"('group', {expr.expression.accept(self)})" 

    def visit_literal_expression(self, expr : Literal) -> str:
        return f"({expr.value})"   

    def visit_unary_expression(self, expr : Unary) -> str:
        return f"({expr.operator.value} {expr.right.accept(self)})"   