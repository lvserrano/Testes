import sys
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
)
from PySide6.QtCore import Qt


class MarkdownCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculadora de Preço de Venda")
        self.setGeometry(100, 100, 360, 250)

        # Layout principal
        layout = QVBoxLayout()

        # Campo para o preço mínimo (Pmz)
        self.label_preco_minimo = QLabel("Preço Mínimo (Pmz):")
        self.input_preco_minimo = QLineEdit()
        self.input_preco_minimo.setPlaceholderText("Digite o preço mínimo (Pmz)")
        layout.addWidget(self.label_preco_minimo)
        layout.addWidget(self.input_preco_minimo)

        # Campo para a margem objetiva (Markdown)
        self.label_markdown = QLabel("Margem Objetiva (Markdown) %:")
        self.input_markdown = QLineEdit()
        self.input_markdown.setPlaceholderText("Digite a margem objetiva em %")
        layout.addWidget(self.label_markdown)
        layout.addWidget(self.input_markdown)

        # Botão para calcular o preço de venda
        self.botao_calcular = QPushButton("Calcular")
        self.botao_calcular.clicked.connect(self.calcular_preco_venda)
        layout.addWidget(self.botao_calcular)

        # Label para exibir o resultado
        self.label_resultado = QLabel("Resultado:")
        self.label_resultado.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label_resultado)

        # Configuração do layout
        self.setLayout(layout)

    def calcular_preco_venda(self):
        try:
            # Substitui vírgulas por pontos e tenta converter para float
            preco_minimo_text = self.input_preco_minimo.text().replace(",", ".")
            markdown_text = self.input_markdown.text().replace(",", ".")

            preco_minimo = float(preco_minimo_text)
            markdown = float(markdown_text)

            # Verifica se a margem é 100%
            if markdown == 100:
                self.label_resultado.setText(
                    "Erro: Uma margem de 100% resulta em preço de venda infinito."
                )
                return

            # Verifica se a margem é maior que 100% e exibe um aviso
            if markdown > 100:
                aviso = "Aviso: A margem objetiva é maior que 100%. O cálculo será feito normalmente."
            else:
                aviso = ""

            # Calcula o preço de venda
            preco_venda = preco_minimo / (1 - markdown / 100)
            lucro_liquido = preco_venda - preco_minimo

            # Exibe o resultado na mesma janela
            self.label_resultado.setText(
                f"{aviso}\nPreço de Venda: R$ {preco_venda:.2f}\nLucro Líquido: R$ {lucro_liquido:.2f}"
            )
        except ValueError:
            self.label_resultado.setText(
                "Erro: Verifique se os valores digitados são numéricos."
            )
        except Exception:
            self.label_resultado.setText(
                "Erro: Ocorreu um problema ao calcular o preço de venda."
            )


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MarkdownCalculator()
    window.show()

    sys.exit(app.exec())
