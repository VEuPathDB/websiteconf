
node('durian') {

    try {
        stage('checkout') {
            checkout(
                    [
                        $class: 'GitSCM',
                        branches: [[name: "*/scm_group"]],
                        extensions: [[
                            $class: 'RelativeTargetDirectory',
                            relativeTargetDir: websiteconf
                            ]],
                            userRemoteConfigs: [[
                                credentialsId: '2dfe5e9c-d974-47b5-a060-34f57039268b',
                                url: git@github.com:VEuPathDB/websiteconf.git
                            ]]
                        ]
                    )
            checkout(
                    [
                        $class: 'GitSCM',
                        branches: [[name: "*/master"]],
                        extensions: [[
                            $class: 'RelativeTargetDirectory',
                            relativeTargetDir: tsrc
                            ]],
                            userRemoteConfigs: [[
                                credentialsId: '2dfe5e9c-d974-47b5-a060-34f57039268b',
                                url: git@github.com:VEuPathDB/tsrc.git
                            ]]
                        ]
                    )


        }
        stage('build') {
            sh 'env'
        }
        



    }


}


