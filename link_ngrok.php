<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
  $content = $_POST['content'];
  $file = fopen('link_ngrok.txt', 'w');
  fwrite($file, $content);
  fclose($file);
  echo 'Lưu nội dung thành công';
}
?>
