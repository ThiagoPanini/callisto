/* --------------------------------------------------------
ARQUIVO: variables.tf

Arquivo de variáveis definidas para configurar todas as
declarações de recursos necessários neste projeto Terraform.
-------------------------------------------------------- */

variable "flag_create_s3_bucket" {
  description = "Flag que habilita a criação de um bucket S3 para armazenamento dos arquivos das tabelas a serem criadas."
  type        = bool
  default     = true
}

variable "s3_bucket_name_prefix" {
  description = "Nome do bucket S3 onde os arquivos das tabelas serão armazenados. Importante: o valor desta variável será concatenado com o ID da conta e o nome da região para no formato '{var.s3_bucket_name_prefix}-{account_id}-{region_name}'"
  type        = string
  default     = "callisto-table-files"
}
