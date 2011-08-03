<?php

function rand_except($from, $to, array $exceptions) {
    sort($exceptions); // lets us use break; in the foreach reliably
    $number = rand($from, $to - count($exceptions)); // or mt_rand()
    foreach ($exceptions as $exception) {
        if ($number >= $exception) {
            $number++; // make up for the gap
        } else /*if ($number < $exception)*/ {
            break;
        }
    }
    return $number;
}

?>
