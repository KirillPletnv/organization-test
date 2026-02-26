#!/bin/bash

URL="http://localhost:8000"
KEY="secret-api-key-12345"

echo "======================================"
echo "Проверка API справочника организаций"
echo "======================================"

echo -e "Проверяем список зданий"
echo "======================================"
curl -H "X-API-Key: $KEY" "$URL/buildings/" | json_pp

echo -e "Проверяем здание с ID=1"
echo "======================================"
curl -H "X-API-Key: $KEY" "$URL/buildings/1" | json_pp

echo -e "Проверяем организации в здании 1"
echo "======================================"
curl -H "X-API-Key: $KEY" "$URL/buildings/1/organizations" | json_pp

echo -e "Проверяем список деятельностей"
echo "======================================"
curl -H "X-API-Key: $KEY" "$URL/activities/" | json_pp

echo -e "Проверяем деятельность с ID=1"
echo "======================================"
curl -H "X-API-Key: $KEY" "$URL/activities/1" | json_pp

echo -e "Проверяем организации по деятельности 'Еда'"
echo "======================================"
curl -H "X-API-Key: $KEY" "$URL/activities/1/organizations/" | json_pp

echo -e "Проверяем список всех организаций"
echo "======================================"
curl -H "X-API-Key: $KEY" "$URL/organizations/" | json_pp

echo -e "Проверяем организацию с ID=1"
echo "======================================"
curl -H "X-API-Key: $KEY" "$URL/organizations/1" | json_pp

echo -e "Проверяем поиск организаций по названию 'Мясной'"
echo "======================================"
curl -H "X-API-Key: $KEY" "$URL/organizations/search/?q=%D0%9C%D1%8F%D1%81%D0%BD%D0%BE%D0%B9" | json_pp

echo -e "Проверяем организации в прямоугольнике"
echo "======================================"
curl -H "X-API-Key: $KEY" "$URL/organizations/nearby/?lat_min=55.70&lat_max=55.80&lon_min=37.50&lon_max=37.70" | json_pp

echo -e "\n======================================"
echo "✅ Проверка завершена"
echo "======================================"
