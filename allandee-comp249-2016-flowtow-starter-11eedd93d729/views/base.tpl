<!DOCTYPE html>
<html lang="en">
  <head>
    <title>{{title}}</title>
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <link rel='stylesheet' href='../static/style.css' type='text/css'>
  </head>

  <body>

    <div class="container">
        <div class='top'>

            <ul class='nav'>
                <li>
                    <a id="logo" href="/">FlowTow</a>
                </li>
                <li><a href="/my">My Images</a></li>
                <li><a href="/about">About this site</a></li>

                % if session:
                <form method="post" id="logoutform" action="/logout">
                    <li>
                        Logged in as {{name}}
                    </li>
                    <li>
                        <input type="submit" value="LOGOUT" class="logbutton">
                    </li>
                </form>
                % else:
                <form method="post" id="loginform" action="/login">
                    <li>Nick:
                        <input name="nick">
                    </li>
                    <li>Password:
                        <input type="password" name="password">
                    </li>
                    <li>
                        <input type="submit" value="LOGIN" class="logbutton">
                    </li>
                </form>

                % end
            </ul>

        </div>
    </div>

    <div>
	 {{!base}}
    </div>

  </body>
</html>
