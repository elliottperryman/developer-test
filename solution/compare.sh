for i in {1..99};
    do
        echo "Iteration: $i"
        give-me-the-odds ../examples/example$i/empire.json ../examples/example$i/millennium-falcon.json
        jq '.odds' < ../examples/example$i/answer.json 
        echo ""
        sleep 0.5

    done;
