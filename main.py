import helper
from send_mail import *
from unidecode import unidecode
from load_participants import *


if __name__ == '__main__':

    # helper.pdf_generator("Wany Mayara da Silva Santos")
    # helper.merge_pdf("files/certificado.pdf", "files/modelo-certificado.pdf", "files/saida-certificado.pdf")

    lista = load("data/avaliadores.xlsx")

    for aluno in lista:
        nomeAluno = unidecode(str(aluno[2]).upper())
        data = aluno[0]
        helper.pdf_generator(nomeAluno, data)
        email = aluno[1]
        helper.merge_pdf("files/modelos/certificado.pdf", "files/modelos/modelo-certificado.pdf",
                         "files/avaliadores/"+nomeAluno.replace(" ","_")+"_certificado.pdf")

        send(email, '[SERTÂO CIÊNCIA] - Certificado Avaliadores',
              'Olá '+nomeAluno+', estamos enviando em anexo o seu certificado de participação como avaliador(a) no evento. Informe-nos através deste e-mail, caso alguma informação esteja incorreta.',
            files=["files/avaliadores/"+nomeAluno.replace(" ","_")+"_certificado.pdf"])