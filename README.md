<h1>Demo Webservice</h1>
<p>The web service uses <strong>Django 1.6.1</strong> and <strong>Django REST Framework 2</strong> and <strong>SQLite</strong> database.  The Django REST Framework was chosen as it has a lot of in-built functionality for authentication, permissions, URL routing, etc. SQLite is the default database and is fine for the requirement.</p>
<ol>
    <li>
        <h2>Register a client</h2>
        <p>A user must already exist in the database to authenticate against. If the user is successfully authenticated a token is returned.</p>
        <p><code>curl -X POST http://127.0.0.1:8000/register/ -d 'username=&lt;username&gt;&amp;password=&lt;password&gt;'</code></p>
    </li>
    <li>
        <h2>Store data</h2>
        <p>You can store data using a POST request, passing the authorisation token in the HTTP header.<br>
            Django REST Framework does not yet support composite primary keys, which in this case is the key name, so a user could receive a warning that the key already exists, even if it was created by another user.</p>
        <p><code>curl -X POST -H "Athorization: Token <token>" http://127.0.0.1:8000/pairs/ -d 'key=&lt;key name&gt;&amp;value=&lt;key value&gt;'</code></p>
    </li>
    <li>
        <h2>Retrieve data</h2>
        <p>Key/value pairs can be retrieved by passing the key name, with the authorisation token in the HTTP header. If no key name is passed all key/value pairs belonging to the authenticated user are returned.</p>
        <p>All key/value pairs:<br>
            <code>curl -H "Authorization: Token <token>" http://127.0.0.1:8000/pairs/</code><br>
            Single key/value pair:<br>
            <code>curl -H "Authorization: Token <token>" http://127.0.0.1:8000/pairs/&lt;key name&gt;/</code></p>
    </li>
</ol>
