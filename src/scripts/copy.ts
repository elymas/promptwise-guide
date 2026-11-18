const toast = document.querySelector<HTMLElement>('.toast');
let timer: ReturnType<typeof setTimeout>;
document.querySelectorAll<HTMLButtonElement>('[data-copy]').forEach(button => {
  button.addEventListener('click', async () => {
    const container = button.closest('[data-card]') || button.closest('section');
    const pre = container?.querySelector<HTMLElement>('[data-prompt]');
    if (!pre) return;
    let message = '프롬프트를 복사했습니다.';
    try { await navigator.clipboard.writeText(pre.textContent || ''); }
    catch { const range = document.createRange(); range.selectNodeContents(pre); const selection=window.getSelection();selection?.removeAllRanges();selection?.addRange(range);message='본문을 선택했습니다. Ctrl/Cmd+C로 복사하세요.'; }
    if(toast) {toast.textContent=message;toast.classList.add('visible');clearTimeout(timer);timer=setTimeout(()=>toast.classList.remove('visible'),3000);}
  });
});
