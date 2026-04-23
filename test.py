class CategoriaSimples:
    def __init__(self, name):
        self.name = name

cat = CategoriaSimples("Eletrônicos")

print(cat)          # O que o print mostra?
print(str(cat))     # O que o str() mostra?
print([cat])        # O que uma lista com ele mostra?



import uuid

class Category:
    def __init__(self, name, description=""):
        self.id = uuid.uuid4()
        self.name = name
        self.description = description

    def __str__(self):
        return f"NOME: {self.name}"

    def __repr__(self):
        return f"DEBUG: Category(id={self.id}, name={self.name})"

cat = Category("Livros", "Literatura Brasileira")

# 1. Uso para o Usuário (Chama o __str__)
print(cat) 
# Saída: NOME: Livros

# 2. Uso para o Programador (Chama o __repr__)
# Quando o objeto está dentro de uma lista, o Python usa o __repr__
lista_de_categorias = [cat]
print(lista_de_categorias)
# Saída: [DEBUG: Category(id=a1-b2..., name=Livros)]