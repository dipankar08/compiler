# Somple C
echo "Running test ...."
curl -X POST -H "Content-Type: application/json" -d '{"lang":"C", "code":"#include <stdio.h>\nint main()\n{\n   printf(\"Hello, World!\");\n   return 0;\n}"}' http://0.0.0.0:80/run

#Simple C++
echo "Running test ...."
curl -X POST -H "Content-Type: application/json" -d '{"lang":"C++", "code":"#include <iostream>\nint main()\n{\n   std::cout<<\"Hello World\";\n   return 0;\n}\n"}' http://0.0.0.0:80/run

#Simple C++ with Loop
echo "Running test ...."
curl -X POST -H "Content-Type: application/json" -d '{"lang":"C++", "code":"#include <iostream>\nint main()\n{\n   while(1);\n   return 0;\n}\n"}' http://0.0.0.0:80/run

#Simple C++ with input
echo "Running test ...."
curl -X POST -H "Content-Type: application/json" -d '{"lang":"C++", "input":"1987", "code":"#include <iostream>\nusing namespace std;\nint main()\n{\n   int i=0;\n   cin>>i;\n   cout<<i;\n   return 0;\n}"}' http://0.0.0.0:80/run

# Simple C++11 Features
echo "Running test ...."
curl -X POST -H "Content-Type: application/json" -d '{"lang":"C++", "code":"#include <iostream>\n#include<vector>\nint main()\n{\n   std::vector<int> vec ={1,2,3,4};\n   for( auto v:vec){\n       std::cout<<v<<std::endl;\n   }\n}"}' http://0.0.0.0:80/run

# Simple C++ Crash
echo "Running test ...."
curl -X POST -H "Content-Type: application/json" -d '{"lang":"C++", "code":"#include <iostream>\nvoid foo(){\n    throw 0;\n}\nint main()\n{\n    foo();\n}\n"}' http://0.0.0.0:80/run

# Simple C++ Crash BT
echo "Running test ...."
curl -X POST -H "Content-Type: application/json" -d '{"lang":"C++", "code":"#include <iostream>\nvoid foo(){\n    throw 0;\n}\nint main()\n{\n    foo();\n}\n"}' http://0.0.0.0:80/crashbt

# Simple C++ Memory leaks.
echo "Running test ...."
#TODO ...

# Simple Java
echo "Running test ...."
curl -X POST -H "Content-Type: application/json" -d '{"lang":"Java", "code":"public class Solution\n{\n\tpublic static void main(String[] args) {\n\t\tSystem.out.println(\"Hello World!\");\n\t}\n}"}' http://0.0.0.0:80/run
