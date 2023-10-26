for i in {1..4};
    do
        give-me-the-odds ../examples/example$i/empire.json ../examples/example$i/millennium-falcon.json
        cat ../examples/example$i/answer.json 
        echo ""

    done;
