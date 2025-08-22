from app.core.firebase import db, firebase_admin
import firebase_admin
import re
import google.generativeai as gemini

admin = firebase_admin

#-------------------------------------------------------------SALVAR AGENDA-------------------------------------------------------------#
def indentificar_tipo_refeicao(hora: str) -> str:
    hora_int = int(hora.split(':')[0])
    if 6 <= hora_int < 11:
        return "Café Da Manhã"
    elif 11 <= hora_int < 15:
        return "Almoço"
    elif 15 <= hora_int < 19:
        return "Lanche"
    else:
        return "Jantar"

def validar_e_formatar_horario(hora: str) -> str:
    """
    Valida e formata o horário no formato HH:MM.
    :param hora: Horário fornecido pelo usuário.
    :return: Horário formatado no formato HH:MM ou levanta uma exceção se inválido.

    """
    try:
        partes = hora.split(":")
        if len(partes) != 2:
            raise ValueError("Formato de horário inválido. Use HH:MM.")

        hora_int = int(partes[0])
        minuto_int = int(partes[1])

        if not (0 <= hora_int < 24) or not (0 <= minuto_int < 60):
            raise ValueError("Horário fora dos limites válidos.")

        return f"{hora_int:02}:{minuto_int:02}"
    except Exception as e:
        raise ValueError(f"Erro ao validar o horário: {str(e)}")

async def salvar_agenda(refeicao, hora, id_user):
    """
    Salva o agendamento no banco de dados Firebase.
    :param refeicao: Nome da refeição.
    :param hora: Horário agendado no formato "HH:mm".
    :param id_user: ID do usuário.

    """
    try:
        hora_formatada = validar_e_formatar_horario(hora)

        tipo_refeicao = indentificar_tipo_refeicao(hora_formatada)
        if not refeicao or not hora:
            print("❌ Erro: Refeição ou hora não informados.")
            return

        ref = db.reference(f"users/{id_user}/diaries")

        novo_agendamento = {
            "tipo_refeicao": tipo_refeicao,
            "refeicao": refeicao,
            "hora": hora_formatada,
            "progress": {
                "0": False,
                "1": False,
                "2": False,
                "3": False,
                "4": False,
                "5": False,
                "6": False
            }
        }

        ref.push(novo_agendamento)

        print(f"✅ Agendamento salvo para o usuário {id_user}")
        return {"resposta":"Agendado com sucesso!"}
    except ValueError as e:
        print(f"❌ Erro ao salvar agendamento: {str(e)}")
        return {"resposta":"Erro ao agendar, tente novamente."}

#-------------------------------------------------------------ATUALIZAR NOME USUARIO-----------------------------------------------------------#
async def update_name_user(args, id_user):
    try:
        ref = db.reference(f"users/{id_user}")
        ref.update({"nome": args["nome"]})
        print("✅ Nome atualizado com sucesso!")
        return {"resposta": "Nome atualizado com sucesso!"}
    except Exception as e:
        print(f"❌ Erro ao atualizar nome: {str(e)}")
        return {"resposta": "Erro ao atualizar nome, tente novamente."}
    
#-------------------------------------------------------------CALCULAR CALORIAS----------------------------------------------------------------#

async def calculate_calories(args, id_user):
    try:
        peso = args["peso"]
        altura = args["altura"]
        idade = args["idade"]
        sexo = args["sexo"]
        meta = args["objetivo"]

        prompt = f"Calcule as calorias diárias para um usuário com peso {peso} kg, altura {altura} m, idade {idade} anos e sexo {sexo} e que possui uma meta de {meta}."
        model_calorias = gemini.GenerativeModel("gemini-2.0-flash", system_instruction="Você deve apenas retornar numero")
        gemini_response = await model_calorias.generate_content_async(prompt)

        calorias = gemini_response.text.strip()
        if not calorias.isdigit():
             return {"resposta": "Erro ao calcular as calorias. Resposta inválida do Gemini."}

        calorias = int(calorias)
        print(f"✅ Calorias calculadas: {calorias}")
        return {"resposta": f"As calorias diárias recomendadas são: {calorias} kcal."}
    except Exception as e:
        print(f"❌ Erro ao calcular calorias: {str(e)}")
        return {"resposta": "Erro ao calcular calorias, tente novamente."}
    
    #-------------------------------------------------------------ATUALIZAR-----------------------------------------------------------#
