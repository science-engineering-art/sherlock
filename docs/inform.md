# Informe

## Preprocesamiento

- tokenizo para obtener los términos indexados
- teniendo en cuenta que cada doc tiene asociado una lista con los términos indexados, construyo matriz de terminos (cols) y documentos(rows) para llevar la frecuencia de cada término en cada documento
- calculo el tf de cada término en cada documento
- calculo el idf de cada término de los docs
- luego calculo los pesos de cada término en cada documento `tf[i][j] * idf[i]`

## Query

- hago el mismo prepocesamiento con el documento, exceptuando el calculo de los pesos de cada término de la consulta
- para el cálculo de los pesos de cada término de la consulta se utiliza la medida de suavizado `a = 0.4` para amortizar la contribución de la frecuencia del término `w[i][q] = (a + (1-a)*f[i][q]/max(f[_][q])*log(N/n_i)`
- utilizando la fórmula de similitud del coseno se haya la cercanía entre el vector consulta y cada vector documento `sim(d[j], q) = (w[i][j] * w[i][q]) / (|w[i][j]| * |w[i][q]|)`
- se almacenan dichos valores para luego hacer un ranking de los documentos teniendo en cuenta su relevancia ante la consulta
