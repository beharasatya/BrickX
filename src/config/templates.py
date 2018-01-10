tpl_start = '''<html>
  <head>
      <title>BrickX</title>
	  <link rel="stylesheet" href="/styles.css">	  
  </head>
  <body>'''

tpl_form_cmp = '''
    <form method="post" action="/test/output" align="center" id="test_ip">

        <fieldset align="center">
        <legend align="center">Text Input</legend> <br>
			<br/>
			<b>Enter the test cases</b> 			
			<br/><br/>
			<textarea name="test_data" form="test_ip" rows='8' cols='30'></textarea>
			<br/><br/>
			<input id="searchbox" type='submit' value='Submit'>
        </fieldset>
        <p>
		    <pre>
		        <code style=display:block;white-space:pre-wrap>
		        {res_tag}
		        </code>
		    </pre>
		</p>
    </form>
    
    '''

tpl_br = '''<br/> <br/>'''

p_tag = '''<p><pre><code style=display:block;white-space:pre-wrap>{txt}</pre></p>'''

auth_tag = '''<p>By <i>{author}</i></p>'''

title_tag = '''<p><a href='{url}' target="_blank"><b>{title}</b></a></p>'''

tpl_end = '''</body>
         </html> '''

tpl_home = tpl_start + tpl_form_cmp.format(res_tag='') + tpl_br  + tpl_end

tpl_404 = '''
        <h1>404</h1>
        <h2>Oops! Page Not Found</h2>
        <p>Sorry, but you are looking for something that isn't here.</p> '''