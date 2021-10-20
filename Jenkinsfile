
node('durian') {

    try {
        stage('checkout') {
            checkout(
                    [
                        $class: 'GitSCM',
                        branches: [[name: "*/master"]],
                        extensions: [[
                            $class: 'RelativeTargetDirectory',
                            relativeTargetDir: 'websiteconf'
                            ]],
                            userRemoteConfigs: [[
                                credentialsId: '3cf5388f-54e2-491b-a7fc-83160dcab3e3',
                                url: 'git@github.com:VEuPathDB/websiteconf.git'
                            ]]
                        ]
                    )
            checkout(
                    [
                        $class: 'GitSCM',
                        branches: [[name: "*/master"]],
                        extensions: [[
                            $class: 'RelativeTargetDirectory',
                            relativeTargetDir: 'tsrc'
                            ]],
                            userRemoteConfigs: [[
                                credentialsId: '3cf5388f-54e2-491b-a7fc-83160dcab3e3',
                                url: 'git@github.com:VEuPathDB/tsrc.git'
                            ]]
                        ]
                    )


        }
        stage('build') {
            sh '''
            virtualenv -p python3 make_yaml_env
            . ./make_yaml_env/bin/activate
            pip install -r websiteconf/requirements.txt
            cd websiteconf
            ./make_yaml.py -m ../tsrc/manifest.yml -o /var/www/software.apidb.org/siteconf/site-conf.yaml
            '''
        }




    }
    catch (exc) {
        throw exc
    }


}


