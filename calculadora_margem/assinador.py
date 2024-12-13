import sys
import subprocess
import os
import json
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QFormLayout,
    QLineEdit,
    QPushButton,
    QFileDialog,
    QLabel,
    QDialog,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QScreen


class CertificateSignerApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Assinador de Scripts com Certificado")
        self.setFixedSize(500, 300)

        # Centralizando a janela na tela
        self.center()

        # Layout principal
        layout = QVBoxLayout()

        # Exibe a label para mostrar status
        self.label = QLabel("Selecione um script para assinar ou crie um certificado.")
        layout.addWidget(self.label)

        # Botões
        self.select_file_button = QPushButton("Selecionar Script")
        self.select_file_button.clicked.connect(self.select_file)
        layout.addWidget(self.select_file_button)

        self.sign_button = QPushButton("Assinar Script")
        self.sign_button.clicked.connect(self.sign_file)
        self.sign_button.setEnabled(False)
        layout.addWidget(self.sign_button)

        self.create_cert_button = QPushButton("Criar Certificado")
        self.create_cert_button.clicked.connect(self.create_certificate)
        layout.addWidget(self.create_cert_button)

        self.setLayout(layout)

        self.cert_info = None
        self.load_cert_info()

    def center(self):
        # Função para centralizar a janela na tela
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        window_geometry = self.frameGeometry()
        center_position = screen_geometry.center() - window_geometry.center()
        self.move(center_position)

    def select_file(self):
        # Abre o diálogo para selecionar um arquivo
        file, _ = QFileDialog.getOpenFileName(
            self,
            "Selecionar Script",
            "",
            "Arquivos Executáveis (*.exe *.bat *.py *.sh)",
        )
        if file:
            self.selected_file = file
            self.label.setText(f"Arquivo selecionado: {self.selected_file}")
            self.sign_button.setEnabled(True)

    def sign_file(self):
        if not self.cert_info:
            self.label.setText(
                "Certificado não encontrado. Crie um certificado primeiro."
            )
            return

        openssl_path = "C:\\Program Files\\OpenSSL-Win64\\bin\\openssl.exe"
        cert_info = self.cert_info

        # Gerar a chave privada da CA (se não existir)
        ca_key_path = "private/my_ca.key"
        if not os.path.exists(ca_key_path):
            subprocess.run(
                [
                    openssl_path,
                    "genpkey",
                    "-algorithm",
                    "RSA",
                    "-out",
                    ca_key_path,
                    "-aes256",
                ]
            )

        # Gerar o certificado da CA (se não existir)
        ca_cert_path = "my_ca.crt"
        if not os.path.exists(ca_cert_path):
            subprocess.run(
                [
                    openssl_path,
                    "req",
                    "-new",
                    "-x509",
                    "-key",
                    ca_key_path,
                    "-out",
                    ca_cert_path,
                    "-days",
                    "3650",
                    "-subj",
                    f"/C={cert_info['C']}/ST={cert_info['ST']}/L={cert_info['L']}/O={cert_info['O']}/CN={cert_info['CN']}",
                ]
            )

        # Gerar a chave privada para o script
        script_key_path = "private/my_script.key"
        subprocess.run(
            [openssl_path, "genpkey", "-algorithm", "RSA", "-out", script_key_path]
        )

        # Gerar o CSR (Certificate Signing Request) para o script
        csr_path = "my_script.csr"
        subprocess.run(
            [openssl_path, "req", "-key", script_key_path, "-new", "-out", csr_path]
        )

        # Assinar o CSR com a CA
        signed_cert_path = f"{self.selected_file}.signed.crt"
        subprocess.run(
            [
                openssl_path,
                "ca",
                "-in",
                csr_path,
                "-out",
                signed_cert_path,
                "-cert",
                ca_cert_path,
                "-keyfile",
                ca_key_path,
            ]
        )

        self.label.setText(f"Arquivo assinado com sucesso: {signed_cert_path}")

    def create_certificate(self):
        cert_dialog = CreateCertDialog(self)
        cert_dialog.exec()

        # Se o certificado foi criado com sucesso
        if cert_dialog.cert_info:
            self.cert_info = cert_dialog.cert_info
            self.save_cert_info()
            self.label.setText("Certificado criado e salvo com sucesso!")

    def load_cert_info(self):
        cert_file = "cert_info.json"
        if os.path.exists(cert_file):
            with open(cert_file, "r") as f:
                self.cert_info = json.load(f)

    def save_cert_info(self):
        cert_file = "cert_info.json"
        with open(cert_file, "w") as f:
            json.dump(self.cert_info, f, indent=4)


class CreateCertDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Criar Certificado")
        self.setFixedSize(400, 200)

        # Centralizando a janela do diálogo
        self.center()

        # Layout para o formulário
        layout = QFormLayout()

        self.C_field = QLineEdit()
        self.C_field.setText("BR")  # País Brasil
        layout.addRow("País (C) *", self.C_field)

        self.ST_field = QLineEdit()
        self.ST_field.setText("Minas Gerais")  # Estado Minas Gerais
        layout.addRow("Estado (ST)", self.ST_field)

        self.L_field = QLineEdit()
        self.L_field.setText("Espera Feliz")  # Cidade Espera Feliz
        layout.addRow("Cidade (L)", self.L_field)

        self.O_field = QLineEdit()
        self.O_field.setText("Vivenci Supermercado LTDA")  # Nome da Empresa
        layout.addRow("Organização (O)", self.O_field)

        self.CN_field = QLineEdit()
        self.CN_field.setText("Vivenci Supermercado LTDA")  # Nome Comum
        layout.addRow("Nome Comum (CN) *", self.CN_field)

        self.ok_button = QPushButton("Criar Certificado")
        self.ok_button.clicked.connect(self.create_cert)
        layout.addRow(self.ok_button)

        self.setLayout(layout)

        self.cert_info = None

    def center(self):
        # Função para centralizar a janela de diálogo
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        window_geometry = self.frameGeometry()
        center_position = screen_geometry.center() - window_geometry.center()
        self.move(center_position)

    def create_cert(self):
        # Coleta os dados inseridos pelo usuário
        C = self.C_field.text().strip()
        CN = self.CN_field.text().strip()

        if not C or not CN:
            self.parent().label.setText("País e Nome Comum são obrigatórios!")
            return

        self.cert_info = {
            "C": C,
            "ST": self.ST_field.text().strip(),
            "L": self.L_field.text().strip(),
            "O": self.O_field.text().strip(),
            "CN": CN,
        }

        self.accept()


# Função principal para rodar o app
def main():
    app = QApplication(sys.argv)
    window = CertificateSignerApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
