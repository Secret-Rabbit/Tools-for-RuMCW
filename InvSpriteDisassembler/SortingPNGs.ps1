# Раскладывает файлы с расширением .png по папкам с заданным количеством элементов в алфавитном порядке
$NumberItemsInFolder = 50
$PrefixFolder = "Part"
# таблица всех файлов в с расширением.png
$PngsList = (Get-ChildItem -Name -Path ./*.png)
# обнуление количества папок
$NumFolder = 0
# перечисление всех файлов из $PngsList
for ($i = 0; $i -lt $PngsList.Count; $i++) {
	# создание папок по количеству сортируемых файлов
	if ($i % $NumberItemsInFolder -eq 0) {
		# создание папок
		$NumFolder++
		$NameFolder = $PrefixFolder + " " + $NumFolder
		New-Item -Path . -Name $NameFolder -ItemType "directory"
	}
	# создание пути файла
	$TransferFileName = "./" + $PngsList[$i]
	# копирование файла в нужную папку
	Move-Item -Path $TransferFileName -Destination $NameFolder
}