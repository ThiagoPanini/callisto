/* --------------------------------------------------------
ARQUIVO: locals.tf

Arquivo responsável por declarar variáveis/valores locais
capazes de auxiliar na obtenção de informações dinâmicas
utilizadas durante a implantação do projeto, como por
exemplo, o ID da conta alvo de implantação ou o nome da
região.
-------------------------------------------------------- */

locals {
  # Extraindo ID da conta e nome da região
  account_id  = data.aws_caller_identity.current.account_id
  region_name = data.aws_region.current.name

  # Definindo nome de bucket S3 alvo de armazenamento dos arquivos das tabelas
  s3_bucket_name = "${var.s3_bucket_name_prefix}-${local.account_id}-${local.region_name}"

  # Definindo paths de diretórios de arquivos e schemas
  data_files_dir   = "${path.module}/assets/files"
  data_schemas_dir = "${path.module}/assets/schemas"

  # Criando dicionário contendo informações completas dos arquivos (tabelas)
  data_files_names = fileset(local.data_files_dir, "*")
  tables_map = {
    for file_name in local.data_files_names :
    file_name => {
      file_name = file_name
      file_path = "${local.data_files_dir}/${file_name}"
      schema    = yamldecode(file("${local.data_schemas_dir}/${element(split(".", file_name), 0)}.yaml"))
    }
  }
}
