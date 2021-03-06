var target_index;
var guess_input_text;
var guess_input;
var finished = false;
var guesses = 0;
var color_array = ['blue', 'cyan', 'gold', 'green', 'magenta', 'orange', 'red', 'white']

function do_game() {
  target_index = Math.floor(Math.random() * color_array.length);
  while (!finished) {
    guess_input_text = prompt("I am thinking of one of there colors:\n\n"+
                              color_array.join() + "\n\n"+
                              "What color I am thinking of?");
    guess_input = guess_input_text.toLowerCase().trim();
    guesses++;
    finished = check_guess();
  }
}

function check_guess() {
  var guess_index = color_array.indexOf(guess_input);
  if (-1 == guess_index) {
    alert("I don't know that color.\n\n"+
          "Please enter one of these colors: " + color_array.join());
    return false;
  }
      //alert ("guess="+guess_index+"   -   target="+target_index);
  if (guess_index > target_index) {
    alert("Hint: your color alphabetically higher than mine.\n\nPlease guess again.");
    return false;
  }
  if (guess_index < target_index) {
    alert("Hint: your color alphabetically lower than mine.\n\nPlease guess again.");
    return false;
  }

  var myBody = document.getElementsByTagName('body')[0];
  myBody.style.background = color_array[target_index];

  alert("Congratulations! The color was "+color_array[target_index] +
        "\nIt took you " + guesses + " guesses to finish the game.\n\n"+
        "You can see the color in the background.");
  return true;
}
