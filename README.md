<h1> <strong>MOZART</strong>: A Toy Programming Language Designed for Music Programming</h1>
<img src="https://image.spreadshirtmedia.net/image-server/v1/products/T1459A839PA4459PT28D118739808W7911H10000/views/1,width=550,height=550,appearanceId=839,backgroundColor=F2F2F2/wolfgang-amadeus-mozart-sticker.jpg", alt="Mozart", width=200, height=200>

<h2> How To Use The Interpreter</h2>
<ol>
  <li>Install a compatible version of Python. Recommended a version greater than 3.8.</li>
  <li>[Optional, but recommended] Create a new python virtual environment and use it.</li>
  <li>Install the requirements.txt: pip install -r requirements.txt</li>
  <li>Run the mozart.py file passing as a parameter the path to the code to be interpreted. Example: python mozart.py ./my_code.mozart. There is flag to show the final state after runnnig the program. Read the mozart argparser file for more details.</li>
  <li>If you want to run the tests just execute the mozart test runner file. The default directory for tests is currently "/data/mozart_test_files/command_interpretation".</li>
</ol>
<h2> How To Code In Mozart</h2>
<p>There is a document describing the language. The document contains the lexer, parser, ast, semantic analysis and interpreter details. The document with detailed descriptions will be published asap.</p>

<h2>To Do</h2>

<ul>Add more test cases.</ul>
<ul>Finish the implementation of all built-in functions.</ul>
<ul>Publish the document with the language description.</ul>
<ul>Make the programming language accept user defined functions.</ul>
