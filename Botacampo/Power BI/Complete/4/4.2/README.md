1. Dupliquei tabela "financials" e renomeei a original à "financial-original" para servir de backup.
2. Dupliquei tabela "financials" e renomeei a "financials (2)" para "D_Produtos".

3. Na "D_Produtos" usei "Group By" na coluna "Products", trocando de "Base" para "Advanced" e fiz as agregações:

	-"Average" em "Units Sold" para obter a média de unidades vendidas.
	-"Average" em "Sale Price" para obter a média de valor de vendas.
	-"Median" em "Sale Price" para obter a mediana de valor de vendas.
	-"Max" em "Sale Price" para obter o valor máximo de vendas.
	-"Min" em "Sale Price" para obter o valor mínimo de vendas.

4. Na aba "Add Column" Adicionei uma coluna de índice do 0, renomeando-a para "ID_produto".
5. Renomeei a coluna "Products" para "Produtos".

6. Dupliquei a tabela "financials" e renomeei a "financials (2)" para D_Produtos_Detalhes.
7. Selecionei as colunas "Product", "Discount Band", "Units Sold", "Manufacturing Price", e "Sale Price" e utilizei o menu do click direito para remover as outras colunas.
8. Na aba "Add Column" utilizei o "Conditional Column" usando "If" "Product" "equals" para cada produto para adicionar seus respectivos ids.
9. Removi a coluna "Product".

10. Dupliquei a tabela "financials" e renomeei a cópia para "D_Descontos".
11. Mesmo procedimento que a "7.", mas com "Product", "Discount Band", e "Discount".
12. Mesmo procedimento que a "8." e "9.".

13. Dupliquei a tabela "financials" e renomeei a "financials (2)" para D_Produtos_Detalhes.
14. Mesmo que "7.", mas com "Product", "Gross Sales", "COGS", e "Date".
15. Mesmo que "8." e "9.".

16. Duplicar 'financials' e renomear a copia à "F_Vendas"
17. Mesmo que "7." mas com "Segment", "Country", "Product", "Discount Band", "Units Sold", "Sales", "Profit", e "Date.
18. Mesmo que "8."
19. Na "Add Column" Adicionei uma coluna de índice e nomeei de "SK_ID"

20. Salvei o Power Query

21. No Power BI, em "Modal View" em "New Table" usei a expressão

	D_Calendario = CALENDAR(MIN(financials[Date]), MAX(financials[Date]))

Para criar um calendario com datas indo da menor data da financials, até a maior.

22. No Power Query criei um surrogate key id para cada tabela, sendo: "D_Produtos_Detalhes[SK_ID]", "D_Descontos[SK_ID]", "D_Detalhes[SK_ID]".

23. No Power BI relacionei "D_Produtos[id_produtos]" com "F_Vendas[id_Produto]" e os sk_ids mencionados em "22." para "F_Vendas[SK_ID]".

24. Exclui a backup "financials-original" já que não foi necessaria, e esta apenas gastando espaço.

25. Adicionei algumas outras colunas para a D_Data, sendo essas: 
Ano = YEAR(D_Calendario[Date]), 
Mes = YEAR(D_Calendario[Date]),
Nome de Mes = FORMAT(D_Calendario[Date],"MMMM", "pt-br"),
Dia = DAY(D_Calendario[Date]),
Dia da Semana = WEEKDAY(D_Calendario[Date]),
Nome do Dia = FORMAT(D_Calendario[Date],"dddd","pt-br"),
Trimestre = QUARTER(D_Calendario[Date])