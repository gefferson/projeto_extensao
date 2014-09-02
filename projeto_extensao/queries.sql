CREATE VIEW pessoa_fisica_academico AS
SELECT u.login AS matricula,
      p.email AS email,
      CONCAT_WS("$", "sha1", SUBSTRING(MD5(u.senha), 1, 12), SHA1(CONCAT(SUBSTRING(MD5(u.senha), 1, 12), u.senha))) AS password,
      u.tipo,
      p.cpf,
      p.identidade AS rg,
      p.orgaoExpIdentidade AS orgao_expedidor,
      p.nacionalidade,
      IF(
       LOCATE(' ', TRIM(p.nome)) > 0,
       SUBSTRING(TRIM(p.nome), 1, LOCATE(' ', TRIM(p.nome)) - 1),
       TRIM(p.nome)
      ) AS first_name,
      IF(
       LOCATE(' ', TRIM(p.nome)) > 0,
       SUBSTRING(TRIM(p.nome), LOCATE(' ', TRIM(p.nome)) + 1),
       NULL
      ) AS last_name,
      p.fone1 as telefone,
      lat.nomeTurma as turma,
      cu.nome AS curso,
      end.rua, end.numero, end.complemento, end.bairro, end.cep, end.municipio
FROM secretaria.pessoas p
   LEFT JOIN secretaria.usuarios u ON u.pessoas_idpessoas=p.idpessoas
       LEFT JOIN secretaria.alunos a ON a.pessoas_idpessoas = p.idpessoas
           LEFT JOIN secretaria.listaAlunosTurma lat ON lat.idalunos = a.idalunos
               LEFT JOIN secretaria.matricula m ON m.alunos_idalunos=a.idalunos
                   LEFT JOIN secretaria.curso cu ON cu.idcurso=m.curso_idcurso
                       LEFT JOIN secretaria.endereco end ON end.idendereco = p.endereco_idendereco;




CREATE VIEW usuario_academico AS SELECT u.login AS matricula, CONCAT_WS("$", "sha1", SUBSTRING(MD5(u.senha), 1, 12),
SHA1(CONCAT(SUBSTRING(MD5(u.senha), 1, 12), u.senha))) AS password, p.email AS email, u.tipo as tipo
FROM secretaria.usuarios u LEFT JOIN secretaria.pessoas p ON u.pessoas_idpessoas = p.idpessoas