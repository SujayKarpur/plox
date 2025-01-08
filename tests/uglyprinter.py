from expr import Visitor, Binary, Grouping, Literal, Unary




class Printer(Visitor[str]):

    def visit_binary_expression(self, expr : Binary) -> str: 
        return f"({expr.operator} {expr.left.accept(self, expr.left)} {expr.right.accept(self, expr.right)})" 

    def visit_grouping_expression(self, expr : Grouping) -> str:
        return f"('group', {expr.expression.accept(self, expr.expression)})" 

    def visit_literal_expression(self, expr : Literal) -> str:
        return f"({expr.value})"   

    def visit_unary_expression(self, expr : Unary) -> str:
        return f"({expr.operator} {expr.right.accept(self, expr.right)})"   